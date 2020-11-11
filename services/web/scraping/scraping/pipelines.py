# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import datetime
import scrapy
import psycopg2
from django.conf import settings


class ForecastPipeline:
    def __init__(self):
        self.counter = 0

    def open_spider(self, spider: scrapy.Spider):
        # Connect to postgresql
        DATABASE = settings.DATABASES["default"]
        self.connection = psycopg2.connect(
            host=DATABASE["HOST"],
            port=DATABASE["PORT"],
            dbname=DATABASE["NAME"],
            user=DATABASE["USER"],
            password=DATABASE["PASSWORD"],
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):

        jst = datetime.timezone(datetime.timedelta(hours=+9), "jst")
        row_update_time = item["update_time"]
        update_hour = int(re.findall(r"\d{2}", row_update_time)[1])
        now = datetime.datetime.now()
        today = datetime.datetime.now(jst)
        update_time = datetime.datetime(
            year=today.year, month=today.month, day=today.day, hour=update_hour
        )

        area = item["area"]
        prefecture = item["prefecture"]
        city = item["weather_city"][0]

        # Check if location data about area and pref is in the database
        area_sql = "SELECT id FROM accounts_area WHERE name=%s"
        self.cursor.execute(area_sql, (area,))
        area_id = self.cursor.fetchone()
        pref_sql = "SELECT id FROM accounts_prefecture WHERE name=%s"
        self.cursor.execute(pref_sql, (prefecture,))
        prefecture_id = self.cursor.fetchone()
        if area_id is None or prefecture_id is None:
            raise scrapy.exceptions.DropItem("Invalid location.")

        # Check if scraped data is new one
        latest_forecast_sql = "SELECT * FROM closet_forecast WHERE area_id=%s AND prefecture_id=%s AND created_at=%s"
        self.cursor.execute(latest_forecast_sql, (area_id, prefecture_id, update_time))
        latest_forecast_data = self.cursor.fetchone()
        if latest_forecast_data:
            raise scrapy.exceptions.DropItem("Already inserted this items.")

        clothes_city_list = item["clothes_info"][::2]
        clothes_index_list = item["clothes_info"][1::2]

        weather = item["weather"][0]
        highest_temp = int(item["highest_temp"][0][:-1])
        lowest_temp = int(item["lowest_temp"][0][:-1])
        rain_chance = item["rain_chance"][0]
        rain_chance = int(rain_chance.replace("\n        ", "").replace("%    ", ""))
        i = clothes_city_list.index(city)
        index = clothes_index_list[i]

        # Check if a scraped index value is in the database
        clothes_index_sql = "SELECT id FROM closet_clothesindex WHERE value=%s"
        self.cursor.execute(clothes_index_sql, (index,))
        clothes_index_id = self.cursor.fetchone()
        if clothes_index_id is None:
            raise scrapy.exceptions.DropItem("Invalid clothes index")

        # Check if a weather is in closet_weatherelement table.
        # Get its id if there is. Raise if not so.
        if len(weather) == 4:
            weather_list = [weather[0], weather[1:3], weather[-1]]
        elif len(weather) == 1:
            weather_list = [weather]
        else:
            raise scrapy.exceptions.DropItem("Scraped Unknown Weather")

        weather_element_ids = []
        for weather_check in weather_list:
            check_sql = "SELECT id FROM closet_weatherelement WHERE name=%s"
            self.cursor.execute(check_sql, (weather_check,))
            weather_element_id = self.cursor.fetchone()
            if weather_element_id:
                weather_element_ids.append(weather_element_id)
            else:
                raise scrapy.exceptions.DropItem("Scraped Unknown Weather")

        if len(weather_element_ids) == 1:
            weather_element_ids += [None, None]
        elif len(weather_element_ids) == 3:
            pass
        else:
            raise scrapy.exceptions.DropItem("Scraped Unknown Weather")

        # Delete previous data
        self.cursor.execute(
            "DELETE FROM closet_forecast WHERE area_id=%s AND prefecture_id=%s",
            (area_id, prefecture_id),
        )

        # Insert scraped data into the database
        insert_sql = "INSERT INTO closet_forecast (area_id, prefecture_id, first_weather_id, weather_change_id, second_weather_id, highest_temp, lowest_temp, rain_chance, clothes_index_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        self.cursor.execute(
            insert_sql,
            (
                area_id,
                prefecture_id,
                weather_element_ids[0],
                weather_element_ids[1],
                weather_element_ids[2],
                highest_temp,
                lowest_temp,
                rain_chance,
                clothes_index_id,
                update_time,
            ),
        )
        self.connection.commit()
        self.counter += 1

        # return f"Row: {row_update_time}\nUhour: {update_hour}\nNow: {now}\nJST: {today}\nUpdate Time: {update_time}"
        return f"Scraped {self.counter}/{update_time}"
