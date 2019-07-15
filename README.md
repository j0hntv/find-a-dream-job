# find_a_dream_job
Script for searching and comparing programmers' salaries on hh.ru and superjob.ru sites.
```
+HeadHunter Москва------+------------------+------------------+
| Язык программирования | Найдено вакансий | Средняя зарплата |
+-----------------------+------------------+------------------+
| Kotlin                | 92               | 174420           |
| Scala                 | 39               | 171401           |
| Swift                 | 83               | 168646           |
| Go                    | 118              | 160935           |
| Java                  | 454              | 159134           |
| Haskell               | 8                | 157500           |
| R                     | 94               | 150557           |
| Bash                  | 93               | 143945           |
| C#                    | 351              | 142457           |
| Python                | 379              | 139676           |
| Ruby                  | 78               | 138757           |
| SQL                   | 977              | 133956           |
| C                     | 174              | 131880           |
| C++                   | 81               | 131543           |
| JS                    | 991              | 130004           |
| 1С                    | 431              | 127117           |
| Php                   | 584              | 120425           |
| Lua                   | 13               | 115076           |
| Pascal                | 11               | 88545            |
+-----------------------+------------------+------------------+
```
```
+SuperJob Москва--------+------------------+------------------+
| Язык программирования | Найдено вакансий | Средняя зарплата |
+-----------------------+------------------+------------------+
| Java                  | 9                | 123183           |
| Python                | 7                | 116191           |
| C#                    | 14               | 105260           |
| 1С                    | 78               | 102551           |
| SQL                   | 52               | 100867           |
| C++                   | 15               | 100724           |
| Pascal                | 1                | 100000           |
| JS                    | 26               | 97450            |
| Php                   | 23               | 97223            |
| C                     | 5                | 88973            |
| Kotlin                | 0                | 0                |
| Ruby                  | 0                | 0                |
| Go                    | 0                | 0                |
| R                     | 0                | 0                |
| Swift                 | 0                | 0                |
| Scala                 | 0                | 0                |
| Lua                   | 0                | 0                |
| Haskell               | 0                | 0                |
| Bash                  | 0                | 0                |
+-----------------------+------------------+------------------+
```

### How to install

Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To search for jobs on SuperJob, register the application and get the `secret key` [(API SuperJob)](https://api.superjob.ru/). Create environment variables `.env` with secret key. 

```
SUPERJOB_KEY=<SUPERJOB_KEY>
```
### Usage
```
python main.py
```
### Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).
