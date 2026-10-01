# DataScienceLab1: Data Collection & Processing Pipeline

Лабораторна робота зі збору, обробки, аналізу  погодних даних із різних джерел (Web Scraping, REST API, JSON, XML, Unstructured Text/Regex).

---

## ℹ️ Опис проєкту

Проєкт реалізує повний цикл роботи з даними (Data Engineering & Analysis pipeline):
* **Збір даних:** Веб-скрейпінг з Wikipedia та запити до Open-Meteo REST API.
* **Обробка та парсинг:** Робота зі структурованими (JSON, XML) та неструктурованими (Regex з текстових звітів) даними.
* **Аналіз:** Обчислення температурних коливань, оцінка рівня вологості, опадів та визначення екстремальних погодних днів.
* **Експорт:** Збереження очищених даних у стандартизовані CSV та JSON файли.

---

## 📁 Структура репозиторію

```text
DS-Lab-1-main/
├── src/
│   ├── __init__.py                    
│   ├── utils.py                      
│   ├── task1_scrape.py               
│   ├── task2_fetch_tokyo_weather.py   
│   ├── task3_complex_weather_analysis.py 
│   ├── task4_weather_summary_export.py   
│   ├── task5_parse_weather_xml.py     
│   ├── task6_extract_weather_data.py  
│   ├── tokyo_weather_complex.json  
│   ├── weather_data.xml            
│   └── weather_report.txt            
├── tests/
│   ├── __init__.py                   
│   ├── test_utils.py              
│   ├── test_task1_scrape.py           
│   ├── test_fetch_tokyo_weather.py    
│   ├── test_complex_weather_analysis.py 
│   ├── test_weather_summary_export.py 
│   ├── test_xml_parsing.py        
│   └── test_regex_extraction.py       
├── .github/
│   ├── workflows/
│   │   └── classroom.yml              
│   └── classroom/
│       └── autograding.json           
├── streamlit_app.py                  
├── setup.bat                        
├── setup.sh                   
├── requirements.txt                 
├── .gitignore               
└── README.md                        
