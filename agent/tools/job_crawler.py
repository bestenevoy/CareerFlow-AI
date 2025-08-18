from sqlalchemy import DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String
from sqlalchemy import func
from sqlalchemy import exc

from loguru import logger
from DrissionPage import WebPage
from pathlib import Path

import time
import datetime
import random
import re
import time
import json
from . import analysis
from ..llm_config import create_default_config

config = create_default_config()
Base = declarative_base()
work_dir = Path(__file__).parent.parent.parent
static_dir = work_dir / 'static' / 'img'

class Job(Base):
    __tablename__ = 'job'
    id = Column(String, primary_key=True, comment="job id")
    jobName = Column(String, comment="职位名称")
    cityName = Column(String, comment="城市")
    areaDistrict = Column(String, comment="区")
    brandName = Column(String, comment="公司名")
    salaryDesc = Column(String, comment="薪资范围")
    link = Column(String, comment="详情页链接")
    desc = Column(String, comment="职位描述，包括岗位要求、岗位职责、工作环境等")
    jobLabels = Column(String, comment="职位标签")
    jobDegree = Column(String, comment="学历")
    brandScaleName = Column(String, comment="公司规模")
    brandStageName = Column(String, comment="公司发展阶段")
    brandIndustry = Column(String, comment="公司行业")
    searchKeyword = Column(String, comment="搜索关键字")
    keywords = Column(String, comment="岗位的技能需求或其他要求关键词")
    crawlTime = Column(DateTime, comment="爬取时间", onupdate=func.now(), server_default=func.now(), nullable=False)

    def date_to_timezone_date(self, date, timezone):
        t = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(t))
        dt = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
        dt8 = dt.astimezone(datetime.timezone(datetime.timedelta(hours=timezone)))
        date = dt8.strftime("%Y-%m-%d %H:%M:%S")
        return date
    
    
    def to_dict(self):
        return {
            "jobId": self.id,
            "jobName": self.jobName,
            "cityName": self.cityName,
            "areaDistrict": self.areaDistrict,
            "brandName": self.brandName,
            "salaryDesc": self.salaryDesc,
            "link": self.link,
            "desc": self.desc,
            "jobLabels": self.jobLabels,
            "jobDegree": self.jobDegree,
            "brandScaleName": self.brandScaleName,
            "brandStageName": self.brandStageName,
            "brandIndustry": self.brandIndustry,
            "searchKeyword": self.searchKeyword,
            "crawlTime": self.date_to_timezone_date(str(self.crawlTime), 8),
        }


class JobCrawler:
    
    def __init__(self):
        # 创建数据库引擎
        # 这里使用SQLite内存数据库，你可以替换为其他数据库的URL
        work_dir = Path(__file__).parent
        db_path = work_dir / 'job.db'
        engine = create_engine(f'sqlite:///{db_path}')
        # 如果要使用文件存储的SQLite数据库，可以使用如下方式：
        # engine = create_engine('sqlite:///jobs.db')

        # 创建所有表
        # Base.metadata.create_all(engine)

        # 创建Session类
        self.db = sessionmaker(bind=engine)()
        self.driver = WebPage('d')

        cities = []
        with open(work_dir / 'citys.json', 'r', encoding='utf-8') as f:
            cities = json.load(f)

        self.cities_dic = {}
        for city in cities:
            self.cities_dic[city['name']] = city['code']

    def get_list(self, post_name: str, city: str, page: int, page_num=5):
        # 监听网站数据包，必须在请求之前先执行
        self.driver.listen.start("/wapi/zpgeek/search/joblist.json")
        self.driver.get(f"https://www.zhipin.com/web/geek/job?query={post_name}&city={city}&page={page}&pageSize=30")
        logger.debug(f"catching page {page} ...")
        # 等待数据包内容加载
        job_ls = []
        for _ in range(page_num):
            self.driver.scroll.to_bottom()
            resp = self.driver.listen.wait()
            job_ls.extend(resp.response.body['zpData']['jobList'])
        # 获取数据包内容
        return job_ls

    def clean_html(self, html_text: str):
        # 去除 <div> 标签
        cleaned_text = re.sub(r'<div[^>]*>', '', html_text)
        # 去除 </div> 标签
        cleaned_text = re.sub(r'</div>', '', cleaned_text)
        # 去除 <br> 标签
        cleaned_text = re.sub(r'<br>', '\n', cleaned_text)
        cleaned_text = re.sub(r'&nbsp;', '', cleaned_text)

        logger.debug(cleaned_text)
        return cleaned_text

    def get_job_details(self, job_id: str):
        job_url = f"https://www.zhipin.com/job_detail/{job_id}.html"
        time.sleep(random.random() * 3)
        logger.debug(job_url)
        self.driver.get(job_url)
        detail = self.driver.eles(".job-sec-text")
        skills = ",".join(self.driver.eles('.job-keyword-list')[0].text.split("\n"))
        return detail[0].html, skills


    def pipeline(self, job_info: list, searchKeyword: str):
        for job in job_info:
            if "K" not in job["salaryDesc"]:
                continue
            details, keywords = self.get_job_details(job["encryptJobId"])
            logger.debug(keywords)
            job_data = {
                "id": job["encryptJobId"],
                "jobName": job['jobName'],
                "salaryDesc": job['salaryDesc'],
                "jobLabels": str(job['jobLabels']),
                "jobDegree": job['jobDegree'],
                "cityName": job['cityName'],
                "brandName": job['brandName'],
                "brandScaleName": job['brandScaleName'],
                "brandStageName": job['brandStageName'],
                "areaDistrict": job['areaDistrict'],
                "brandIndustry": job['brandIndustry'],
                "link": f"https://www.zhipin.com/job_detail/{job['encryptJobId']}.html",
                "searchKeyword": searchKeyword,
                "keywords": keywords,
                "desc": self.clean_html(details)
            }

            max_retries = 5
            for attempt in range(max_retries):
                try:
                    entity = self.db.query(Job).filter(Job.id == job_data['id']).all()
                    if entity:
                        self.db.delete(entity[0])
                        self.db.commit()
                        time.sleep(0.3)
                    self.db.add(Job(**job_data))
                    self.db.commit()
                    time.sleep(0.3)
                    
                    break
                except exc.OperationalError as e:
                    if "database is locked" in str(e):
                        self.db.rollback()
                        if attempt < max_retries - 1:
                            time.sleep(0.1 * (attempt + 1))  # 指数退避
                            continue
                    raise

    def get_jobs(self, jobName: str, cityName: str):
        bench = 1
        job_list = []
        logger.debug(f"get_jobs {jobName} {cityName}")

        job = self.db.query(Job).filter(Job.cityName==cityName, Job.searchKeyword==jobName).first()
        if not job:
            # 没有数据，从网站爬取
            for i in range(bench):
                job_list.extend(self.get_list(jobName, self.cities_dic[cityName], i+1))
            self.pipeline(job_list, jobName)

        # 有数据，从数据库查询
        job_ls = self.db.query(Job).filter(Job.cityName==cityName, Job.searchKeyword==jobName).all()
        return job_ls

    def get_cities_list(self):
        return list(self.cities_dic.keys())

    def box_analysis(self, search_keyword, city_name):
        # 查询所有数据
        job_ls = self.db.query(Job).filter(Job.cityName==city_name, Job.searchKeyword==search_keyword).all()
        data = {}
        for job in job_ls:
            data[job.brandIndustry] = data.get(job.brandIndustry, [])
            data[job.brandIndustry].append(job.salaryDesc)
        file_name = f"{city_name}_{search_keyword}_brandIndustry_and_salaryDesc_box_plot.jpg"
        file_path = f"{static_dir}/{file_name}"
        filename = analysis.gen_box_plot(data, file_path)
        return {
            "img_tag": f"<img src='http://{config.server_url}:12800/img/{file_name}' width='900px'/>",
            "data": data
        }

    def pie_analysis(self, search_keyword, city_name):
        # 查询所有数据
        job_ls = self.db.query(Job).filter(Job.cityName==city_name, Job.searchKeyword==search_keyword).all()
        data = {}
        for job in job_ls:
            data[job.brandIndustry] = data.get(job.brandIndustry, 0)
            data[job.brandIndustry] += 1
        file_name = f"{city_name}_{search_keyword}_brandIndustry_dist_pie_plot.jpg"
        file_path = f"{static_dir}/{file_name}"
        filename = analysis.draw_pie_chart(data, file_path)

        return {
            "img_tag": f"<img src='http://{config.server_url}:12800/img/{file_name}' width='900px'/>",
            "data": data
        }
        
    def wordcloud(self, search_keyword, city_name):
        job_ls = self.db.query(Job).filter(Job.cityName==city_name, Job.searchKeyword==search_keyword).all()
        if not job_ls:
            return "没有找到相关数据"
        data = {}
        for job in job_ls:
            for keyword in job.keywords.split("\n"):
                data[keyword] = data.get(keyword, 0)
                data[keyword] += 1
        file_name = f"{city_name}_{search_keyword}_keywords_wordcloud.png"
        file_path = f"{static_dir}/{file_name}"
        filename = analysis.generate_low_saturation_wordcloud(data, file_path, title=f"{city_name}{search_keyword}相关岗位需求词云")
        return {
            "img_tag": f"<img src='http://{config.server_url}:12800/img/{file_name}' width='900px'>",
            "data": data
        }