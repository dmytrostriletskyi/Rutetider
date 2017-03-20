from django.conf.urls import url
from frameworkrequests import views

urlpatterns = [

    # Rutetider
    url(r'^timetable/$', views.TimetableApplication.as_view()),
    url(r'^timetable/clear_timetable', views.ClearTimetable.as_view()),
    url(r'^timetable/add_lesson', views.AddLesson.as_view()),
    url(r'^timetable/get_lesson', views.GetLessons.as_view()),
    url(r'^timetable/get_all_courses', views.GetAllCourses.as_view()),
    url(r'^timetable/get_all_groups', views.GetAllGroups.as_view()),

    # Subscribers
    url(r'^statistic/$', views.SubscribersApplication.as_view()),
    url(r'^statistic/clear_subscribers', views.ClearSubscribers.as_view()),
    url(r'^statistic/add_subscriber', views.AddSubscriber.as_view()),
    url(r'^statistic/is_subscriber', views.IsSubscriber.as_view()),
    url(r'^statistic/unsubscribe', views.UnSubscribe.as_view()),

    # CurrentDates
    url(r'^currentdates/$', views.CurrentDatesApplication.as_view()),
    url(r'^currentdates/clear_current_dates', views.ClearCurrentDates.as_view()),
    url(r'^currentdates/add_current_dates', views.AddDates.as_view()),
    url(r'^currentdates/get_current_dates', views.GetDates.as_view()),

    # UserPosition
    url(r'^userposition/$', views.UserPositionApplication.as_view()),
    url(r'^userposition/clear_user_position', views.ClearUserPosition.as_view()),
    url(r'^userposition/add_position', views.AddPosition.as_view()),
    url(r'^userposition/get_position', views.GetPosition.as_view()),

    # Statistic
    url(r'^statistics/$', views.StatisticsApplication.as_view()),
    url(r'^statistics/clear_statistics', views.ClearStatistics.as_view()),
    url(r'^statistics/add_statistics', views.AddStatistics.as_view()),
    url(r'^statistics/get_statistics_general', views.GetStatisticsGeneral.as_view()),
    url(r'^statistics/get_statistics_counts', views.GetStatisticsCounts.as_view()),
    url(r'^statistics/get_statistics_between_dates', views.GetStatisticsBetweenDates.as_view()),
    url(r'^statistics/get_statistics_by_point', views.GetStatisticsByPoint.as_view()),
    url(r'^statistics/point_between_dates', views.GetStatisticsByPointBetweenDates.as_view())]
