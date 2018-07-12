# coding:utf-8
import requests
from lxml import etree
from config import pro_city, mysql_config
import urlparse
import urllib2
import urllib
import pymysql.cursors

query_url = "https://lesmills.com.cn/search/index.asp"

connection = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **mysql_config)
for pro, city in pro_city:

    print "crawling:" + pro + city
    page = 1

    res = urllib2.urlopen(
        urllib2.Request(query_url + "?" + urllib.urlencode({"page": page, "City": city, "Province": pro})))

    selector = etree.HTML(res.read())
    total_page = selector.xpath("//a[@class='next']/@href")
    if total_page:
        total_page = int(urlparse.parse_qs(urlparse.urlparse(total_page[0]).query)["page"].pop())
    else:
        total_page = 1
    while page <= total_page:
        print "page:" + str(page)
        res = urllib2.urlopen(
            urllib2.Request(query_url + "?" + urllib.urlencode({"page": page, "City": city, "Province": pro})))
        selector = etree.HTML(res.read())
        sections = selector.xpath("//*[@class='morespace']/section[@class='topic-article-list']")
        sections = [etree.tostring(section, method='html') for section in sections]
        print "this page has " + str(len(sections)) + " items "
        for section in sections:
            section = etree.HTML(section)
            href = section.xpath("//article[@class='topic-article-list__item']/a/@href")
            club_url = urlparse.urljoin(query_url, href[0])
            club_name = section.xpath("//article/p[1]/strong/text()")[0]
            club_lessons = section.xpath("//article/p[3]/span/@labelname")
            club_lessons = [l[12:-1] for l in club_lessons]
            club_alias_id = section.xpath("//article/a[1]/@href").pop()[:-5]
            print club_url, club_name, club_lessons, club_alias_id
            club_res = requests.get(club_url)
            se = etree.HTML(club_res.content)
            detail_area = se.xpath("//div[@class='morespace']/p[1]/text()").pop()[3:].strip()

            with connection.cursor() as cursor:
                sql = "INSERT INTO `club` ( `name`, `province`, `city`, `detail_area`,`club_id`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (club_name, pro, city, detail_area, club_alias_id))
                cursor.execute("SELECT id from `club` WHERE `name`=%s", (club_name,))
                club_id = cursor.fetchone()['id']
                for le in club_lessons:
                    cursor.execute("SELECT id from `lesson` WHERE `name`=%s", (le,))
                    le_id = cursor.fetchone()
                    if not le_id:
                        sql = "INSERT INTO `lesson` ( `name`) VALUES (%s)"
                        cursor.execute(sql, (le,))
                        cursor.execute("SELECT id from `lesson` WHERE `name`=%s", (le,))
                        le_id = cursor.fetchone()
                    le_id = le_id['id']
                    print le_id
                    sql = "INSERT INTO `club_lesson` ( `club_id`,`lesson_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (club_id, le_id))
                    connection.commit()


            print detail_area
            coaches = se.xpath("//div[@class='morespace']/p[@class='topic-article-list__excerpt']")
            if len(coaches) <= 4:
                print "no coaches here"
                continue
            coaches = coaches[4:]
            coaches = [etree.tostring(coach, method='html') for coach in coaches]
            with connection.cursor() as cursor:
                for coach in coaches:
                    s = etree.HTML(coach)
                    coach_name = s.xpath("//p/text()")[0].strip()[:-1].strip()
                    lesson = s.xpath("//p/span/@labelname")[0][12:-1]
                    cursor.execute("SELECT id from `coach` WHERE `name`=%s", (coach_name,))
                    co_id = cursor.fetchone()
                    if not co_id:
                        cursor.execute("INSERT INTO `coach` (`name`) values (%s)", (coach_name,))
                        cursor.execute("SELECT id from `coach` WHERE `name`=%s", (coach_name,))
                        co_id = cursor.fetchone()
                    co_id = co_id['id']
                    cursor.execute("INSERT INTO `club_coach` (`club_id`,`coach_id`) values (%s,%s)", (club_id, co_id))
                    cursor.execute("SELECT id from `lesson` WHERE `name`=%s", (lesson,))
                    lesson_id = cursor.fetchone()
                    if not lesson_id:
                        cursor.execute("INSERT INTO `lesson` (`name`) values (%s)", (lesson, ))
                        cursor.execute("SELECT id from `lesson` WHERE `name`=%s", (lesson,))
                        lesson_id = cursor.fetchone()
                    lesson_id = lesson_id['id']
                    cursor.execute("INSERT INTO `lesson_coach` (`lesson_id`,`coach_id`) values (%s, %s)", (lesson_id, co_id))
                    print coach_name, lesson
                    connection.commit()
        page += 1
        print "----"
