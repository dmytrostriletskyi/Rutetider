from frameworkrequests.rutetider import Timetable, Subscribers, CurrentDates, UserPosition, Statistics
from rest_framework.views import APIView
from django.http import JsonResponse
import datetime


def is_url_out(data, url):
    if url not in data:
        return True


# Timetable
class TimetableApplication(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            rutetider.create_timetable()
            return JsonResponse({
                'Response': 'Singleton application was successfully initialized.',
                'Done': 'Table \'timetable\' has been created in database.',
                'Additional documentation information': 'If table already exists, requests does not re-create it.'},
                status=200)
        else:
            return JsonResponse({'Response': 'Singleton application creation has been failed.'}, status=400)


class ClearTimetable(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            rutetider.clear_timetable()
            return JsonResponse({'Response': 'Table \'timetable\' has been cleared in database.'}, status=200)
        else:
            return JsonResponse({'Response': 'Singleton application creation has been failed.'}, status=400)


class AddLesson(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            rutetider.add_lesson(
                request.data['faculty'], request.data['course'], request.data['group_name'],
                request.data['lesson_date'], request.data['lesson_title'], request.data['lesson_classroom'],
                request.data['lesson_order'], request.data['lesson_teacher'])
            return JsonResponse({'Response': 'Lessons data was successfully added.'}, status=200)
        else:
            return JsonResponse({'Response': 'Lessons data addition has been failed.'}, status=400)


class GetLessons(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            return JsonResponse({
                'lessons': rutetider.get_lessons(request.data['group_name'], request.data['lesson_date'])}, status=200)


class GetAllCourses(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            return JsonResponse({'courses': rutetider.get_all_courses(request.data['faculty'])}, status=200)


class GetAllGroups(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        rutetider = Timetable(database_url)
        if rutetider:
            return JsonResponse({'groups': rutetider.get_all_groups(request.data['faculty'], request.data['course'])},
                                status=200)


# Subscribers
class SubscribersApplication(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        subscribers = Subscribers(database_url)
        if subscribers:
            subscribers.create_subscribers()
            return JsonResponse({
                'Response': 'Subscribers application was successfully initialized.',
                'Done': 'Table \'subscribers\' has been created in database.',
                'Additional documentation information': 'If table already exists, requests does not re-create it.'},
                status=200)
        else:
            return JsonResponse({'Response': 'Subscribers application creation has been failed.'}, status=400)


class ClearSubscribers(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        subscribers = Subscribers(database_url)
        if subscribers:
            subscribers.clear_subscribers()
            return JsonResponse({
                'Response': 'Table \'subscribers\' has been cleared in database.'}, status=200)
        else:
            return JsonResponse({'Response': 'Subscribers application creation has been failed.'}, status=400)


class AddSubscriber(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        subscriber = Subscribers(database_url)
        if subscriber:
            subscriber.add_subscriber(request.data['user_id'], request.data['group_name'])
            return JsonResponse({'Response': 'Subscribers data was successfully added.'}, status=200)


class GetSubscriberGroup(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)
        database_url = request.data['url']
        subscriber = Subscribers(database_url)
        if subscriber:
            return JsonResponse({'group': subscriber.get_subscriber_group(request.data['user_id'])}, status=200)
        else:
            return JsonResponse({'group': subscriber.get_subscriber_group(request.data['user_id'])}, status=400)


class IsSubscriber(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        subscriber = Subscribers(database_url)
        if subscriber:
            return JsonResponse({'Is subscriber': subscriber.is_subscriber(request.data['user_id'])}, status=200)
        else:
            return JsonResponse({'Is subscriber': subscriber.is_subscriber(request.data['user_id'])}, status=400)


class UnSubscribe(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        subscriber = Subscribers(database_url)
        if subscriber:
            subscriber.unsubscribe(request.data['user_id'])
            return JsonResponse({'Response': 'User {0} has been deleted from table \'subscribers\''.format(
                request.data['user_id'])}, status=200)


# CurrentDates
class CurrentDatesApplication(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        dates = CurrentDates(database_url)
        if dates:
            dates.create_current_dates()
            return JsonResponse({
                'Response': 'CurrentDates application was successfully initialized.',
                'Done': 'Table \'current_dates\' has been created in database.',
                'Additional documentation information': 'If table already exists, requests does not re-create it.'},
                status=200)
        else:
            return JsonResponse({'Response': 'CurrentDates application creation has been failed.'}, status=400)


class ClearCurrentDates(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        dates = CurrentDates(database_url)
        if dates:
            dates.clear_current_dates()
            return JsonResponse({
                'Response': 'Table \'current_dates\' has been cleared in database.'}, status=200)
        else:
            return JsonResponse({'Response': 'CurrentDates application creation has been failed.'}, status=400)


class AddDates(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        dates = CurrentDates(database_url)
        if dates:
            dates.add_dates(request.data['today'], request.data['tomorrow'])
            return JsonResponse({'Response': 'Dates ware successfully added.'}, status=200)


class GetDates(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        dates = CurrentDates(database_url)
        if dates:
            return JsonResponse({'dates': dates.get_dates()}, status=200)


# UserPosition
class UserPositionApplication(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.create_user_position()
            return JsonResponse({
                'Response': 'UserPosition application was successfully initialized.',
                'Done': 'Table \'user_position\' has been created in database.',
                'Additional documentation information': 'If table already exists, requests does not re-create it.'},
                status=200)
        else:
            return JsonResponse({'Response': 'UserPosition application creation has been failed.'}, status=400)


class ClearUserPosition(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.clear_user_position()
            return JsonResponse({
                'Response': 'Table \'user_position\' has been cleared in database.'}, status=200)
        else:
            return JsonResponse({'Response': 'UserPosition application creation has been failed.'}, status=400)


class ClearUserData(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.clear_user_data(request.data['user_id'])
            return JsonResponse({
                'Response': 'User data has been cleared from table \'user_position\' in database.'}, status=200)


class SetGettingPosition(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.set_getting_position(request.data['user_id'])
            return JsonResponse({'Response': 'Start position was successfully added.'}, status=200)


class SetFacultyPosition(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.set_faculty_position(request.data['user_id'], request.data['faculty'])
            return JsonResponse({'Response': 'Faculty position was successfully added.'}, status=200)


class SetCoursePosition(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.set_course_position(request.data['user_id'], request.data['course'])
            return JsonResponse({'Response': 'Course position was successfully added.'}, status=200)


class SetGroupPosition(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.set_group_position(request.data['user_id'], request.data['group_name'])
            return JsonResponse({'Response': 'Group position was successfully added.'}, status=200)


class GetFacultyAndCourse(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            return JsonResponse({'Response': position.get_faculty_and_course(request.data['user_id'])}, status=200)


class Verification(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            return JsonResponse({'group': position.verification(request.data['user_id'])}, status=200)


class CancelGettingStarted(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.cancel_getting_started(request.data['user_id'])
            return JsonResponse({
                'Response': 'Start position has been cleared from table \'user_position\' in database.'}, status=200)


class CancelFaculty(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.cancel_faculty(request.data['user_id'])
            return JsonResponse({
                'Response': 'Faculty position has been cleared from table \'user_position\' in database.'}, status=200)


class CancelCourse(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.cancel_course(request.data['user_id'])
            return JsonResponse({
                'Response': 'Course position has been cleared from table \'user_position\' in database.'}, status=200)


class CancelGroup(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            position.cancel_group(request.data['user_id'])
            return JsonResponse({
                'Response': 'Group position has been cleared from table \'user_position\' in database.'}, status=200)


class BackKeyboard(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        position = UserPosition(database_url)
        if position:
            try:
                return JsonResponse({'keyboard': position.back_keyboard(request.data['user_id'])}, status=200)
            except TypeError:
                return JsonResponse({'Response': 'User has no data in database'}, status=200)


# Statistic
class StatisticsApplication(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            statistics.create_statistics()
            return JsonResponse({
                'Response': 'Statistic application was successfully initialized.',
                'Done': 'Table \'statistic\' has been created in database.',
                'Additional documentation information': 'If table already exists, requests does not re-create it.'},
                status=200)
        else:
            return JsonResponse({'Response': 'Statistic application creation has been failed.'}, status=400)


class ClearStatistics(APIView):
    @staticmethod
    def delete(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            statistics.clear_statistics()
            return JsonResponse({
                'Response': 'Table \'statistic\' has been cleared in database.'}, status=200)
        else:
            return JsonResponse({'Response': 'UserPosition application creation has been failed.'}, status=400)


class AddStatistics(APIView):
    @staticmethod
    def put(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        date = datetime.datetime.strptime(request.data['date'], '%d.%m.%Y').date()

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            statistics.add_statistics(request.data['user_id'], request.data['point'], date)
            return JsonResponse({'Response': 'Statistic wars successfully added.'}, status=200)


class GetStatisticsGeneral(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            return JsonResponse({'statistics': statistics.get_statistics_general()}, status=200)


class GetStatisticsCounts(APIView):
    @staticmethod
    def post(request):
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            return JsonResponse({'statistics': statistics.get_statistics_counts()}, status=200)


class GetStatisticsBetweenDates(APIView):
    @staticmethod
    def post(request):
        print('3')
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        date_from = datetime.datetime.strptime(request.data['date_from'], '%d.%m.%Y').date()
        date_to = datetime.datetime.strptime(request.data['date_to'], '%d.%m.%Y').date()

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            return JsonResponse({'statistics': statistics.get_statistics_between_dates(date_from, date_to)}, status=200)


class GetStatisticsByPoint(APIView):
    @staticmethod
    def post(request):
        print('2')
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            return JsonResponse({'statistics': statistics.get_statistics_by_point(request.data['point'])}, status=200)


class GetStatisticsByPointBetweenDates(APIView):
    @staticmethod
    def post(request):
        print('yes')
        if is_url_out(request.data, 'url'):
            return JsonResponse({'Response': 'Database parameter URL in request data not found.'}, status=400)

        date_from = datetime.datetime.strptime(request.data['date_from'], '%d.%m.%Y').date()
        date_to = datetime.datetime.strptime(request.data['date_to'], '%d.%m.%Y').date()

        database_url = request.data['url']
        statistics = Statistics(database_url)
        if statistics:
            return JsonResponse({'statistics': statistics.get_statistics_by_point_between_dates(request.data['point'],
                                date_from, date_to)}, status=200)
