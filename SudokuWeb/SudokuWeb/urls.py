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
    url(r'^SudokuHome/$', views.Sudoku_Home, name='Sudoku_Home'),
    url(r'^FillominoHome/$', views.Fillomino_Home, name='Fillomino_Home'),
   # url(r'^FillominoHome/displayFillomino/$', views.displayFillomino, name='displayFillomino'),
    url(r'^howtoplaySudoku/$', views.howtoplaySudoku, name='howtoplaySudoku'),
    url(r'^about/$', views.about, name='about'),
    url(r'^SudokuHome/genSudoku/$', views.genSudoku, name='generate'),
    url(r'^FillominoHome/genRandFillomino/$', views.genRandFillomino, name='genRandFillomino'),
    url(r'^SudokuHome/genRandSudoku/$', views.genRandSudoku, name='genRandSudoku'),
    url(r'^addPuzzles/$', views.addPuzzles, name='addPuzzles'),
    url(r'^displayFillomino/(\d+)/$', views.displayFillomino, name='displayFillomino'),
    url(r'^displaySudoku/(?P<board_id>\d+)/$', views.displaySudoku, name='displaySudoku'),
    url(r'^displaySudoku/(\d+)/checkSudoku/$', views.checkSudoku, name='checkSudoku'),
    url(r'^displaySudoku/(\d+)/displaySudoku/$', views.displaySudoku, name='checkSudoku'),
    url(r'^displaySudoku/(\d+)/checkSudoku/displaySudoku', views.displaySudoku, name='displaySudoku'),
    url(r'^displaySudoku/(\d+)/checkSudoku/ratingSudoku', views.ratingSudoku, name='rating'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
