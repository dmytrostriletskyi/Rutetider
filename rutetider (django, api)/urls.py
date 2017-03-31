from django.views.generic import RedirectView
from frameworkrequests import views
from django.conf.urls import url


urlpatterns = [

    url(r'^$', RedirectView.as_view(url='https://github.com/DmytryiStriletskyi/Rutetider/wiki')),

    # Rutetider
    url(r'^timetable', views.TimetableApplication.as_view()),
    url(r'^timetable/clear_timetable', views.ClearTimetable.as_view()),
    url(r'^timetable/add_lesson', views.AddLesson.as_view()),
    url(r'^timetable/get_lesson', views.GetLessons.as_view()),
    url(r'^timetable/get_all_courses', views.GetAllCourses.as_view()),
    url(r'^timetable/get_all_groups', views.GetAllGroups.as_view()),

    # Subscribers
    url(r'^subscribers', views.SubscribersApplication.as_view()),
    url(r'^subscribers/clear_subscribers', views.ClearSubscribers.as_view()),
    url(r'^subscribers/add_subscriber', views.AddSubscriber.as_view()),
    url(r'^subscribers/get_subscriber_group', views.GetSubscriberGroup.as_view()),
    url(r'^subscribers/is_subscriber', views.IsSubscriber.as_view()),
    url(r'^subscribers/unsubscribe', views.UnSubscribe.as_view()),

    # CurrentDates
    url(r'^currentdates', views.CurrentDatesApplication.as_view()),
    url(r'^currentdates/clear_current_dates', views.ClearCurrentDates.as_view()),
    url(r'^currentdates/add_current_dates', views.AddDates.as_view()),
    url(r'^currentdates/get_current_dates', views.GetDates.as_view()),

    # UserPosition
    url(r'^userposition', views.UserPositionApplication.as_view()),
    url(r'^userposition/clear_user_position', views.ClearUserPosition.as_view()),
    url(r'^userposition/clear_user_data', views.ClearUserData.as_view()),
    url(r'^userposition/set_getting_position', views.SetGettingPosition.as_view()),
    url(r'^userposition/set_faculty_position', views.SetFacultyPosition.as_view()),
    url(r'^userposition/set_course_position', views.SetCoursePosition.as_view()),
    url(r'^userposition/set_group_position', views.SetGroupPosition.as_view()),
    url(r'^userposition/get_faculty_and_course', views.GetFacultyAndGroup.as_view()),
    url(r'^userposition/verification', views.Verification.as_view()),
    url(r'^userposition/cancel_getting_started', views.CancelGettingStarted.as_view()),
    url(r'^userposition/cancel_faculty', views.CancelFaculty.as_view()),
    url(r'^userposition/cancel_course', views.CancelCourse.as_view()),
    url(r'^userposition/cancel_group', views.CancelGroup.as_view()),
    url(r'^userposition/back_keyboard', views.BackKeyboard.as_view()),

    # Statistic
    url(r'^statistics', views.StatisticsApplication.as_view()),
    url(r'^statistics/clear_statistics', views.ClearStatistics.as_view()),
    url(r'^statistics/add_statistics', views.AddStatistics.as_view()),
    url(r'^statistics/get_statistics_general', views.GetStatisticsGeneral.as_view()),
    url(r'^statistics/get_statistics_counts', views.GetStatisticsCounts.as_view()),
    url(r'^statistics/get_statistics_between_dates', views.GetStatisticsBetweenDates.as_view()),
    url(r'^statistics/get_statistics_by_point', views.GetStatisticsByPoint.as_view()),
    url(r'^statistics/point_between_dates', views.GetStatisticsByPointBetweenDates.as_view())]
