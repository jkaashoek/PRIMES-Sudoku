from django.conf.urls import patterns, include, url
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SudokuWeb.views.home', name='home'),
    # url(r'^SudokuWeb/', include('SudokuWeb.foo.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^howtoplay/$', views.howtoplay, name='howtoplay'),
    url(r'^genSudoku/$', views.genSudoku, name='generate'),
    url(r'^addPuzzles/$', views.addPuzzles, name='addPuzzles'),
    url(r'^displayBoard/(?P<board_id>\d+)/$', views.displayBoard, name='displayBoard'),
    url(r'^displayBoard/(\d+)/checkSudoku/$', views.checkSudoku, name='checkSudoku'),
    url(r'^displayBoard/(\d+)/displayBoard/$', views.displayBoard, name='checkSudoku'),
    url(r'^displayBoard/(\d+)/checkSudoku/displayBoard', views.displayBoard, name='displayBoard'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
