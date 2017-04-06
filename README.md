# Rutetider
[![Build Status](https://travis-ci.org/DmytryiStriletskyi/Rutetider.svg?branch=master)](https://travis-ci.org/DmytryiStriletskyi/Rutetider)
![Python Versions](https://camo.githubusercontent.com/2337a7f5bde4563869e31ce69df4bacfc0b96277/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f74656c6567726170682e737667)

![platforms](https://habrastorage.org/files/c69/e7e/0c0/c69e7e0c07d74a0ebe3b9efdb4556cee.png)

Информация подана более структурировано на русском языке [здесь](https://github.com/DmytryiStriletskyi/Rutetider/wiki/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-Rutetider).

# **Введение в Rutetider**

Rutetider — готовое архитектурное решение для всех видов платформ, поддерживающих http-запросы, в большей степени из-за отсутствия языковых и ресурсных возможностей — для веб, в частности Telegram-bot`ы, в меньшей — из-за нативной предрасположенности — для IOS и Android (часть функционала фреймворка не нужна из-за инструментов «из коробки», например, локального хранилища).

Главными инструментами для разработчиков будут являтся REST-API (например, клиент на Android) и непосредственно сама библиотека, написанная на Python (Telegram-bot) — в зависимости от выбора методов и платформ разработки, а также необходима удаленная база данных (нет необходимости с ней работать, все за вас сделает «Rutetider»), бесплатную и пригодную к использованию в продакшине по объему — на этот счет не беспокойтесь, [здесь](https://github.com/DmytryiStriletskyi/Rutetider/wiki/%D0%91%D0%B0%D0%B7%D1%8B-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%B4%D0%BB%D1%8F-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8) предоставлен гайд по подключению ряда бесплатных инстансов.  

Фреймворк имеет в наличие обязательные и необязательные модули, например, вам в любом случае необходимо работать напрямую с расписанием (заносить пары или уроки, начало и конец по времени, преподавателей и аудитории, или же наоборот — получать расписание, список групп на обределенном курсе и прочее), а вот вести статистику может быть кому-то и ни к чему.

Приложение, архитектуру которого вам необходимо будет соблюдать, состоит из пяти отдельных «экранов», каждый из которого требует на определенном этапе определенных действий от разработчика, опять же — например, на основе введенной группы и даты получить из базы данных расписание на нужный день. И здесь не упущу возможности заверить, что копаться в чем-то сложном не придется, просто необходимо соблюдать шаблон и читать документацию.


Первые три экрана с выбором **меню**, **факультета** и **курса**.

![first_menus](https://habrastorage.org/files/229/b09/03d/229b0903d51640c397ea8c5ae47dc930.png)

Вторые два с выбором **группы** и **дат**.

![last_menus](https://habrastorage.org/files/2f6/e11/409/2f6e11409a2d4980875f0d8893c269f7.png)

# **Компоненты структуры**

Фреймворк предоставляет пять базовых частей, часть из них не являются обязательными, но есть основные, без которых разработка обойтись не может. 

Ниже представлена схема примерная схема работы приложения. Если объяснить главный принцип, то — необходимо следить и записывать на каком этапе (какое меню выбора на экране) находится пользователь, не забывать вносить данные о самом выборе (факультет, курс, группа) и отображать расписание соответсвующим входящим параметрам (получить расписание по такой-то группе и дню).

![schema](https://habrastorage.org/files/db3/3d6/deb/db33d6deb7a84cd982a2c94051a546d1.png)

Все методы и детальная работа с ними будет расписана в [API по ссылке](https://github.com/DmytryiStriletskyi/Rutetider/wiki/Rutetider-API), а ниже вы можете ознакомиться чуть более глубже с тем, что, возможно, потребуется в дальнейшем. Не углубляйтесь в примеры и особенности, важно понять концепцию.

## **Timetable**

Данный модуль фреймворка предназначен непосредственно для контакта с расписанием. Например, вам будет доступен вариант занисения расписания в базу данных:

```python
from rutetider import Timetable

timetable = Timetable(database_url)
timetable.add_lesson('IT', '3', 'PD-31', '18.10', 'Литература', 
                     '451', '2', 'Шевченко Т.Г.')
# params: faculty, course, group_name, lesson_date, lesson_title, 
#         lesson_classroom, lesson_order, lesson_teacher
```

Или же вы захотите получить расписание для вашей группы на определенный день:
```python
schedule = timetable.get_lessons('PD-31', '18.10')
# params: group_name, lesson_date

print(schedule)
# {'lessons': {
#           '3': {'lesson_teacher': 'Шевченко О.В.', 'lesson_classroom': 
#                 '451', 'lesson_order': '3', 'lesson_title': 'Литература'}, 
#           '1': {'lesson_teacher': 'Шульга О.С.', 'lesson_classroom': '118', 
#                 'lesson_order': '1', 'lesson_title': #'Математика'}, 
#           '2': {'lesson_teacher': 'Ковальчук Н.О.', 'lesson_classroom': '200', 
#                 'lesson_order': '2', 'lesson_title': #'Инженерия ПО'}}}
```

## **Subscribers**

![back_button](https://habrastorage.org/files/8a0/065/d6a/8a0065d6a296428e8dc86ff6269a3087.png)

Вы можете имплеменировать данный компонент, который позволит пользователю совершать меньше действий и переходов, и сразу получать расписание по одной кнопке — для этого вам надо, чтобы он подписался на определенную группу (занести эту группу в базу данных), а после, при желании пользоватя получить расписание — отдать ему расписание на сегодняшний и завтрашний день (запросить группу пользователя, запросить расписание по группе и датам).

```objective-c
import UIKit

class ViewController: UIViewController {

    fileprivate let databaseURL = "postgres://nwritrny:VQJnfVmooh3S0TkAghEgA--YOxoaPJOR@stampy.db.elephantsql.com:5432/nwritrny"
    fileprivate let apiURL = "http://api.rutetiderframework.com"
    
    @IBAction func subscribeAction(_ sender: Any) {
        let headers = ["content-type": "application/x-www-form-urlencoded"]
        
        let postData = NSMutableData(data: "url=\(databaseURL)".data(using: .utf8)!)
        postData.append("&user_id=1251252".data(using: .utf8)!)
        postData.append("&group_name=PD-3431".data(using: .utf8)!)
        
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/subscribers/add_subscriber")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "PUT"
        request.allHTTPHeaderFields = headers
        request.httpBody = postData as Data
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error)
            } else {
                let httpResponse = response as? HTTPURLResponse
                print(httpResponse)
            }
        })
        
        dataTask.resume()
    }

    @IBAction func getSubscriptionInfoAction(_ sender: Any) {
    
        let headers = ["content-type": "application/x-www-form-urlencoded"]
        
        let postData = NSMutableData(data: "url=\(databaseURL)".data(using: .utf8)!)
        postData.append("&user_id=1251252".data(using: String.Encoding.utf8)!)
        
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/subscribers/get_subscriber_group")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = headers
        request.httpBody = postData as Data
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error)
            } else if let jsonData = data {
                do {
                    let json = try JSONSerialization.jsonObject(with: jsonData) as? Dictionary<String, Any>
                    print(json?["group"])
                } catch let error{
                    print(error)
                }
            }
        })
        
        dataTask.resume()
    }
    
}
```

## **Current dates**

С помощью данного компонента вы можете управлять датами, которые вам понадобятся при отображении расписания.

```python
import requests
import json

api_url = 'http://api.rutetiderframework.com'

database_url = 'postgres://nwritrny:VQJnfVmooh3S0TkAghEgA--YOxoaPJOR@stampy.db.elephantsql.com:5432/nwritrny'
# Это тестовый параметр, в запросе должна быть ссылка на вашу рабочую базу данных

r = requests.post(api_url + '/currentdates/', data=json.dumps({
	'url': database_url}), headers={'content-type': 'application/json'})

print(r.status_code)
# 200
# Если вы работаете с компонентом впервые, вам необходимо проинициализировать необходимые таблицы, 
# то есть вызвать соответсвующий метод.

r = requests.put('http://api.rutetiderframework.com/currentdates/add_current_dates', data=json.dumps({
	'url': database_url,
	'today': '07.04',
	'tomorrow': '08.04'}), headers={'content-type': 'application/json'})

r = requests.post('http://api.rutetiderframework.com/currentdates/get_current_dates', data=json.dumps({
	'url': database_url}), headers={'content-type': 'application/json'})

print(r.json())
# {'dates': ['07.04', '08.04']}

```
## **User position**

Важным компонентом является получение текущего состояния пользователя, которое позволит грамотно и быстро отобразить следующее состояние или обратное, если пользователь захотел вернуться. Например, если пользователь выбирает группу, то нам необходимо знать, какий выбор пользователь уже сделал (факультет и курс), а если он ошибься курсом — то среагировать на нажатие кнопки «Вернуться назад» ([примеры кода взяты из работающего авторского примера](https://github.com/DmytryiStriletskyi/DuttyBot)).

```python
# Ловим нажатие кнопки пользователем
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or
                     '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or
                     '6 курс' == mess.text or '7 курс' == mess.text, content_types=['text'])
def handle_text(message):
    UserPosition(database_url).set_course_position(str(message.chat.id), message.text[:1])
    # Записывааем в специальный метод «set_course_position» идентификатор пользователя (message.chat.id) и 
    # и собственно выбор (message.text[:1] - '7 курс'[:1] = '7')
    faculty, course = UserPosition(database_url).get_faculty_and_course(str(message.chat.id))
    # «get_faculty_and_course» помогает узнать сделанный выбор пользователя ранее 
    groups_list = Timetable(database_url).get_all_groups(faculty, course)
    # По факультету и курсу получаем список групп и сортируем его
    groups_list.sort()
    keyboard.group_list_by_faculty_and_group(groups_list, message)
    # Выводим на экран (это встроенный метод другой библиотеки, частный случай)
```

«Вернуться назад» в авторском проекте выглядит так.

![back_button](https://habrastorage.org/files/d4a/1da/0ac/d4a1da0acc364c8a88799c490075d90d.png)

Возвращение на одно меню назад реализовывается немного сложнее, поэтому давайте разберем следующее.

![user_position](https://habrastorage.org/files/8a6/9ae/4f0/8a69ae4f026245f3b77b64f0a04ca292.png)

Чтобы знать, какое меню необходимо пользовалю, если он хочет вернуться назад, нам нужно воспользоваться методом 
«back_keyboard», который подскажет на какой позиции остановился пользователь. Из схемы видно, что позиция равна единице (1) — цифре, означающей порядковый номер меню, на котором пользователь «застрял», значит, вернуться надо на индексовую позицию ноль (1 - 1). И еще раз: индекс — какое меня было до предпоследним, позиия пользователя — какое меню сейчас. Как вы отображаете меню и где вы его храните — дело вашего приложения, но получение позиции уже работа фреймворка.

```python
@bot.message_handler(func=lambda mess: 'Вернуться назад' == mess.text, content_types=['text'])
def handle_text(message):
    user_position = UserPosition(database_url).back_keyboard(str(message.chat.id))
    if user_position == 1:
        UserPosition(database_url).cancel_getting_started(str(message.chat.id))
        keyboard.main_menu(message)

    if user_position == 2:
        UserPosition(database_url).cancel_faculty(str(message.chat.id))
        keyboard.get_all_faculties(message)

    if user_position == 3:
        UserPosition(database_url).cancel_course(str(message.chat.id))
        faculty = UserPosition(database_url).verification(str(message.chat.id))
        if faculty != "Загальні підрозділи" and faculty != 'Заочне навчання':
            keyboard.stable_six_courses(message)

        if faculty == "Загальні підрозділи":
            keyboard.stable_one_course(message)

        if faculty == "Заочне навчання":
            keyboard.stable_three_courses(message)

    if user_position == 4:
        UserPosition(database_url).cancel_group(str(message.chat.id))
        faculty, course = UserPosition(database_url).get_faculty_and_course(str(message.chat.id))
        groups_list = Timetable(database_url).get_all_groups(faculty, course)
        groups_list.sort()
        keyboard.group_list_by_faculty_and_group(groups_list, message)
```

То есть при каждом выборе меню вам надо задавать расположение группы, при желании вернуться - отменять расположение и отображать новое меню согласно индексу. Трудно по-началу понять, но другого выбора нет, если вам не доступны какие-то локальные хранилища как телефон пользователя напрямую (IOS, Android).

## **Statistics**

Вы можете легко вести детальную статистику вашего приложения, например, записывать количество выбранного пользователями факультета, а потом с легкостью получать данную цифру и отображать в какую-нибудь админ-панель.

```objective-c
func initializeDatabase() {
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/statistics/")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = headers
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: callback)
        
        dataTask.resume()
    }
    
    func addStatistic() {

        let body = ["url": databaseURL, "user_id": "1251252", "point": "faculty", "date": "06.04.2017"]
        
        var jsonBody: Data?
        
        do {
            jsonBody = try JSONSerialization.data(withJSONObject: body)
        } catch  {
        }
        
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/statistics/add_statistics")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "PUT"
        request.allHTTPHeaderFields = headers
        request.httpBody = jsonBody
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: callback)
        
        dataTask.resume()
    }
    
    func getStatistic() {
        let body = ["url": databaseURL, "user_id": "1251252"]
        var jsonBody: Data?
        do {
            jsonBody = try JSONSerialization.data(withJSONObject: body)
        } catch  {
        }
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/statistics/get_statistics_general")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = headers
        request.httpBody = jsonBody
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: callback)
        dataTask.resume()
    }
    
    func callback(_ data: Data?, _ resp: URLResponse?, _ error: Error?) {
        printResponse(resp, error: error)
        parseResponse(data)
    }
    
    func parseResponse(_ data: Data?) {
        if let jsonData = data {
            do {
                let json = try JSONSerialization.jsonObject(with: jsonData) as? Dictionary<String, Any>
                print(json ?? "json is nil")
            } catch let error{
                print(error)
            }
        }
    }
    
    func printResponse(_ response: URLResponse?, error: Error?)  {
        if (error != nil) {
            print(error!)
        } else {
            let httpResponse = response as? HTTPURLResponse
            print(httpResponse ?? "response is nil")
        }
    }
```
# **Rutetider API**

В зависимости от выбора технологий, языка программирования, сервера и прочих параметров, вам будет ноебходимо выбрать для себя — с каким интерфейсом вы будете работать, они отличаются в зависимости от направления. 
Примеры кода вы уже видели [здесь](https://github.com/DmytryiStriletskyi/Rutetider/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B-%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D1%8B).



## **Python**

Данный путь подойдет разработчикам, которые имеют возможность работать с Python-библиотекой напрямую, например,
Telegram-Bot. Библиотека доступна по ссылке - [«Rutetider API wrapper»](https://pypi.python.org/pypi).

```python
from rutetider import Timetable

timetable = Timetable(database_url)
timetable.add_lesson('IT', '3', 'PD-31', '18.10', 'Программирование', 
                     '451', '2', 'Шевченко Т.Г.')
# params: faculty, course, group_name, lesson_date, lesson_title, 
#         lesson_classroom, lesson_order, lesson_teacher
```

## **REST-API**

Пример на Objective-C.
```objective-c
func addLesson() {

        let body = ["url": databaseURL, "faculty": "IT", "course": "3", "group_name": "PD-31",
        "lesson_date": "18.10", "lesson_title": "Программирование", "lesson_classroom": "451", 
        "lesson_order": "2", "lesson_teacher": "Шевченко Т.Г."]

        var jsonBody: Data?
        
        do {
            jsonBody = try JSONSerialization.data(withJSONObject: body)
        } catch  {
        }
        
        let request = NSMutableURLRequest(url: NSURL(string: "\(apiURL)/timetable/add_lesson")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "PUT"
        request.allHTTPHeaderFields = headers
        request.httpBody = jsonBody
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: callback)
        
        dataTask.resume()
    }
```

Пример на Python.
```python

r = requests.put('http://api.rutetiderframework.com/timetable/add_lesson', data=json.dumps({
	'url': database_url, 'faculty': 'IT', 'course': '3', 'group_name': 'PD-31,
        'lesson_date': '18.10', 'lesson_title': 'Программирование',
        'lesson_classroom': '451', 'lesson_order': '2', 'lesson_teacher': 'Шевченко Т.Г.'}), 
        headers={'content-type': 'application/json'})
```

Вы можете обратить внимание, что отличий в методах почти нет, за исключением подхода программирования, то есть название функции и аргументов через библиотеку соотвествует пути и параметрам в запросе.

## **Правила использования фреймворка**

1. Запрос к REST-API всегда требует параметр «database_url», работа через Python-библиотеку — только при инициализации объекта.
2. Ответ на метод всегда в формате **JSON**.
3. Обращаться к АПИ необходимо по заданому пути:
```
http://api.rutetiderframework.com
```

То есть, если вы хотите использовать метод «add_lesson», в документации сказано, что к которому надо прописывать «/timetable/add_lesson», у вас должно получиться следующее.
```
http://api.rutetiderframework.com/timetable/add_lesson
```
4. Вы можете заносить даты (и время) только в строковом формате (ничего не мешает вам заносить строковый объект формата даты, а потом конвертировать), но давайте согласуемся, что отмечать только дату будем в таком виде — "26.04.2017" (день.месяц.год).

# **Базы данных для разработки**

Параметр «database_url» необходим, чтобы фреймворк куда-то записывал данные и откуда-то их брал, едиснтвенным верным подходом в решении это задачи явялется регистрация своего аккаунта на каком-нибудь ресурсе, который предоставляет бесплатные инстансы под хранение данных.

## **Elephant SQL**

Адрес — https://www.elephantsql.com

Регистрация — https://customer.elephantsql.com/login (можно через Google или Github)

![Register](https://habrastorage.org/files/015/ea1/bcf/015ea1bcfc9141e4abe06987a572290f.png)
![Register](https://habrastorage.org/files/dc7/0ae/548/dc70ae5485f54af09c67ea508bbb7453.png)
![Details](https://habrastorage.org/files/9e4/f0c/248/9e4f0c24826a41e69e93570b2436f5b6.png)

Необходимый параметр в виде строки — URL.
```python
database_url = 'postgres://nwritrny:VQJnfVmooh3S0TkAghEgA--YOxoaPJOR@stampy.db.elephantsql.com:5432/nwritrny'
```

Интерфейс приятный и выглядит так.

![Console](https://habrastorage.org/files/b77/173/583/b77173583e4b474aa31177597f8ff434.png)

# API

Перед использование API, пожалуйста, ознакомьтесь с [правилами](https://github.com/DmytryiStriletskyi/Rutetider/wiki/Rutetider-API#%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-%D1%84%D1%80%D0%B5%D0%B9%D0%BC%D0%B2%D0%BE%D1%80%D0%BA%D0%B0).

Ниже представлены таблицы, разделенные на четыре колонки, первая пара из которых относится к REST-API (метод и путь), вторая к Python-библиотеке (класс и метод класса).

## **create_timetable**

Используйте этот метод для инициализации таблици для расписания, использовать данный метод в Python-библиотеке не обязательно, при создании объекта класса таблица создается автоматически.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | timetable/ | Timetable | create_timetable()

**Parameters:** database_url

***

## **clear_timetable**

Используйте данный метод для полного очищения таблицы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | timetable/clear_timetable | Timetable | clear_timetable()

**Parameters:** database_url

***

## **add_lesson**

Используйте данный метод для добавления данных об одном уроке.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | timetable/add_lesson | Timetable | add_lesson()

**Parameters:** database_url, faculty, course, group_name, lesson_date, lesson_title, lesson_classroom, lesson_order, lesson_teacher

***

## **get_lesson**

Используйте данный метод для получения данных об уроках для определенной группы и дня.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | timetable/get_lesson | Timetable | get_lesson()

**Parameters:** database_url, group_name, lesson_date

***

## **get_all_courses**

Используйте данный метод для получения списка курсов соотвественно указанному факультету.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | timetable/get_all_courses | Timetable | get_all_courses()

**Parameters:** database_url, faculty

***

## **get_all_groups**

Используйте данный метод для получения списка курсов соотвественно указанному курсу и факультету.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | timetable/get_all_courses | Timetable | get_all_groups()

**Parameters:** database_url, faculty, course

***

## **create_subscribers**

Используйте этот метод для инициализации таблици для подписчиков, использовать данный метод в Python-библиотеке не обязательно, при создании объекта класса таблица создается автоматически.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | subscribers/ | Subscribers | create_timetable()

**Parameters:** database_url

***

## **clear_subscribers**

Используйте данный метод для полного очищения таблицы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | subscribers/clear_subscribers | Subscribers | clear_subscribers()

**Parameters:** database_url

***

## **add_subscriber**

Используйте данный метод для добавления подписчика.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | subscribers/add_subscriber | Subscribers | add_subscriber()

**Parameters:** database_url, user_id, group_name

***

## **get_subscriber_group**

Используйте данный метод для получения группы, на которую подписался пользователь.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | subscribers/get_subscriber_group | Subscribers | get_subscriber_group()

**Parameters:** database_url, user_id

***

## **is_subscriber**

Используйте данный метод для проверки, является ли пользователь подписчиком.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | subscribers/is_subscriber | Subscribers | is_subscriber()

**Parameters:** database_url, user_id

***

## **unsubscribe**

Используйте данный метод для отмени подписки определенному пользователю.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | subscribers/unsubscribe | Subscribers | unsubscribe()

**Parameters:** database_url, user_id

***


## **create_current_dates**

Используйте этот метод для инициализации таблици для дат, использовать данный метод в Python-библиотеке не обязательно, при создании объекта класса таблица создается автоматически.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | currentdates/ | CurrentDates | create_current_dates()

**Parameters:** database_url

***

## **clear_current_dates**

Используйте данный метод для полного очищения таблицы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | currentdates/clear_current_dates | CurrentDates | clear_current_dates()

**Parameters:** database_url

***

## **add_current_dates**

Используйте данный метод для добавления дат на сегодняшний и завтрашний день.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | currentdates/add_current_dates | CurrentDates | add_current_dates()

**Parameters:** database_url, today, tomorrow

***

## **get_current_dates**

Используйте данный метод для получения сегодняшнего и завтрашнего дня.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | currentdates/get_current_dates | CurrentDates | get_current_dates()

**Parameters:** database_url

***


## **create_userposition**

Используйте этот метод для инициализации таблици для управления состоянием пользователя, использовать данный метод в Python-библиотеке не обязательно, при создании объекта класса таблица создается автоматически.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | userposition/ | UserPosition | create_userposition()

**Parameters:** database_url

***

## **clear_user_position**

Используйте данный метод для полного очищения таблицы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | userposition/clear_user_position | UserPosition | clear_user_position()

**Parameters:** database_url

***

## **clear_user_data**

Используйте данный метод для очищения всех данных о позиции пользователя.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | userposition/clear_user_data | UserPosition | clear_user_data()

**Parameters:** database_url, user_id

***

## **set_getting_position**

Используйте данный метод для добавления позиции, когда пользователь совершил переход с первого меня во второе (нажал на кнопку получения расписания и остановился на выборе факультета).

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/set_getting_position | UserPosition | set_getting_position()

**Parameters:** database_url, user_id

***

## **set_faculty_position**

Используйте данный метод для добавления позиции, когда пользователь выбрал факультет и остановился на выборе курса.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/set_faculty_position | UserPosition | set_faculty_position()

**Parameters:** database_url, user_id, faculty

***

## **set_course_position**

Используйте данный метод для добавления позиции, когда пользователь выбрал курс и остановился на выборе группы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/set_course_position | UserPosition | set_course_position()

**Parameters:** database_url, user_id, course

***

## **set_group_position**

Используйте данный метод для добавления позиции, когда пользователь выбрал группу и остановился на выборе даты расписания и прочих возможных функций.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/set_group_position | UserPosition | set_group_position()

**Parameters:** database_url, user_id, group_name

***

## **get_faculty_and_course**

Используйте данный метод для получения указанного факультета и курса пользователем ранее.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | userposition/get_faculty_and_course | UserPosition | get_faculty_and_course()

**Parameters:** database_url, user_id

***

## **verification**

Используйте данный метод для получения группы, указанной пользователем (название из-за особенности метода).

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | userposition/verification | UserPosition | verification()

**Parameters:** database_url, user_id

***

## **cancel_getting_started**

Используйте данный метод для отмены позиции пользоватя, когда он перешел к выбору факультета. Фактически вы удаляете все записи в базе данных о выборе и «начинаете с чистого листа».

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | userposition/cancel_getting_started | UserPosition | cancel_getting_started()

**Parameters:** database_url, user_id

***

## **cancel_faculty**

Используйте данный метод для отмены позиции пользоватя, когда он перешел к выбору курса, тогда вы собственными инструментами возвращаете его на повторный выбор факультета и отменяете его уже проделанный выбор пользователем.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/cancel_faculty | UserPosition | cancel_faculty()

**Parameters:** database_url, user_id

***

## **cancel_course**

Используйте данный метод для отмены позиции пользоватя, когда он перешел к выбору группы, тогда вы собственными инструментами возвращаете его на повторный выбор курса и отменяете его уже проделанный выбор пользователем.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/cancel_course | UserPosition | cancel_course()

**Parameters:** database_url, user_id

***

## **cancel_group**

Используйте данный метод для отмены позиции пользоватя, когда он перешел к последнему меню, тогда вы собственными инструментами возвращаете его на повторный выбор группы и отменяете его уже проделанный выбор пользователем.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/cancel_group | UserPosition | cancel_group()

**Parameters:** database_url, user_id

***

## **back_keyboard**

Используйте данный метод для получение индекса и позиции меню при нажатии кнопки возврата к предыдущему выбору. [По ссыке](https://github.com/DmytryiStriletskyi/Rutetider/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B-%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D1%8B#user-position) детальное пояснение метода.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | userposition/back_keyboard | UserPosition | back_keyboard()

**Parameters:** database_url, user_id

***

Параметр «point», который вы встретите в дальнейшем, это произвольное текстовое значение,
передавать на месте которого необходимо какое-либо действие. Например, если вы хотите, чтобы
велась статистика по факультетам, то используйте метод добавления статистики и передавайте на место
этой переменной что-то вроде 'faculty', в итоге по этому же значению вы эту статистику и получите.

## **create_statistics**

Используйте этот метод для инициализации таблици для статистики, использовать данный метод в Python-библиотеке не обязательно, при создании объекта класса таблица создается автоматически.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/ | Statistics | create_statistics()

**Parameters:** database_url

***

## **clear_statistics**

Используйте данный метод для полного очищения таблицы.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 DELETE | statistics/clear_statistics | Statistics | clear_statistics()

**Parameters:** database_url

***

## **add_statistics**

Используйте данный метод для добавления статистики.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 PUT | statistics/add_statistics | Statistics | add_statistics()

**Parameters:** database_url, user_id, point, date

***

## **get_statistics_general**

Используйте данный метод для получения общей статистики вашего приложения.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/get_statistics_general | Statistics | get_statistics_general()

**Parameters:** database_url

***

## **get_statistics_counts**

Используйте данный метод для получения количества записанных вами point`ов в соответстии к каждому типу (например, для факультета, курса и подписки).

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/get_statistics_counts | Statistics | get_statistics_counts()

**Parameters:** database_url

***

## **get_statistics_between_dates**

Используйте данный метод для получения статистики за определенный период (от и до какого-то дня).

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/get_statistics_between_dates | Statistics | get_statistics_between_dates()

**Parameters:** database_url, date_from, date_from

***

## **get_statistics_by_point**

Используйте данный метод для получения статистики по определенному point`у.

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/get_statistics_by_point | Statistics | get_statistics_by_point()

**Parameters:** database_url, point

***

## **point_between_dates**

Используйте данный метод для получения статистики по определенному point`у в определенный период (от и до какого-то дня).

 method| url | class | method
 --------    | ----------------- | --------    | -----------------
 POST | statistics/point_between_dates | Statistics | point_between_dates()

**Parameters:** database_url, point, date_from, date_to

***
