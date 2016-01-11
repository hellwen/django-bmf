/*!
django BMF
*/

(function($){
    if(!$.bmf){
        $.bmf = new Object();
    };

    // Keys
    $.bmf.KEYS = {
        ESC: 27,
        TAB: 9,
        RETURN: 13,
        UP: 38,
        DOWN: 40
    };

    $.bmf.AJAX = {
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        crossDomain: false,
        dataType: 'json',
        error: function(jqXHRm, textStatus, errorThrown) {
            console.log( errorThrown+" ("+textStatus+")" );
        },
        statusCode: {
            403: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 403\n You don't have permission to view this page") );
            },
            404: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 404\n Page not found") );
            },
            405: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 405\n Method not allowed") );
            },
            500: function(jqXHRm, textStatus, errorThrown) {
                if (jqXHRm.responseText == undefined) {
                    alert( gettext("Error 500\n An Error occured while rendering the page") );
                }
                else {
                    alert( jqXHRm.responseText );
                }
            }
        }
    };
})(jQuery);

/* calendar */

/*
<div class="form-group">
    <label class="control-label">Employee</label>
    <div>
        <div class="input-group" data-bmf-autocomplete="1">
            <input class="form-control" id="bmf_NAME-value" placeholder="VALUE" type="text">
        </div>
        <input autocomplete="off" id="bmf_NAME" type="text">
    </div>
</div>
*/

(function($){
    $.bmf.autocomplete = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.autocomplete", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.bmf.autocomplete.defaultOptions, options);
            if (base.options.debug) {console.log("init autocomplete")};

            // initialization logic
            base.$el.append('<span class="input-group-btn"></span>');
            base.btn = base.$el.find('.input-group-btn').first();
            base.container = base.$el.parent();

            base.btn.append('<button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-remove"></span></button>');
            // base.btn.append('<button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-plus"></span></button>');

            // base.$el.parent().css('position', 'relative');
            base.container.append('<ul class="dropdown-menu" style="display: none"></ul>');

            base.form = base.$el.parents('form').first();
            base.input = base.$el.children('input[type="text"]').first();
            base.hidden = base.container.children('input[type="hidden"]').first();
            base.dropdown = base.container.children('ul').first();
            base.input.attr('value', base.input.attr('placeholder'));
            base.timeout = false;

            // initialization logic
            // TODO ===============================================================================
            base.input.on('focus', function () {
                base.input.attr('value', '');
                base.getList();
            });
            base.input.on('blur', function () {
                window.setTimeout(function() { base.destroyList(); }, 100);
            });
            base.btn.children().on('click', function () {
                base.input.attr('value', '');
                base.input.attr('placeholder', '');
                base.hidden.attr('value', '');
            });
            base.$el.on('keyup',function () {
                base.getList();
            });
   
            $(document).keydown(function(e){
                if (e.keyCode == $.bmf.KEYS.ESC) {
                    base.destroyList();
                }
            });
        }

        // TODO ===================================================================================


    base.makeList = function(data) {
      base.dropdown.html('');
      $.each( data, function( index, obj ) {
        base.dropdown.append('<li><a href="#'+obj.pk+'">'+obj.value+'</a></li>');
      });
      base.dropdown.find('a').on('click', function (event) {
    		clicked = $(this).attr('href').match('[^#/]+$');
        base.hidden.val(clicked);
        base.input.val( $(this).html());
        base.input.attr('placeholder', $(this).html());
        base.destroyList();
        event.preventDefault();
        base.changed();
      });
      base.dropdown.css("display","block");
    };
    
    base.destroyList = function () {
      base.input.attr('value', base.input.attr('placeholder'));
      base.dropdown.css("display","none");
    };

    base.changed = function() {
      var data = {};
      data.field = base.hidden.attr('id')
      data.form = base.form.serialize();
      //console.log(data.form);

      $.ajax({
        url: base.form.attr('action').split('?')[0]+"form/?changed",
        dataType: 'json',
        type: 'post',
        data: data,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }).done(function( data, textStatus, jqXHR ) {
        $.each( data, function( index, obj ) {
          $('#'+obj.field).attr('value', obj.value);
          $('#'+obj.field).attr('placeholder', obj.value);
        });
      }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log( errorThrown+" ("+textStatus+")" );
      });
    }
    
    base.getList = function() {
        if (base.timeout != false) {
            clearTimeout(base.timeout);
        }
        base.timeout = setTimeout(base.doGetList, base.options.wait);
    }

    base.doGetList = function () {
      base.timeout = false;
      var data = {};
      data.field = base.hidden.attr('id')
      data.form = base.form.serialize();

      data.string = base.input.val();
      if (base.hidden.val() != '') {
        data.selected = base.hidden.val()
      };

      $.ajax({
        url: base.form.attr('action').split('?')[0]+"form/?search",
        dataType: 'json',
        type: 'post',
        data: data,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }).done(function( data, textStatus, jqXHR ) {
        base.makeList(data);
      }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log( errorThrown+" ("+textStatus+")" );
      });
    };


        // TODO =======================================================================================================
      
        // Run initializer
        base.init();
    };

    // default options
    $.bmf.autocomplete.defaultOptions = {
        // Wait 250 ms until the last key action until the request is send
        wait: 250,
        debug: true,
        // Which filter options are submitted
        url: './form/',
    };

    // register as jquery function
    $.fn.bmf_autocomplete = function(options){
        return $(this).find('div.input-group[data-bmf-autocomplete]').each(function(){
            (new $.bmf.autocomplete(this, options));
        });
    };
})(jQuery);

/* calendar */


(function($){
    $.bmf.calendar = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.calendar", base);

        // set strings
        base.monthsOfYear = gettext('January February March April May June July August September October November December').split(' ');
        base.daysOfWeek = gettext('Su Mo Tu We Th Fr Sa').split(' ');
        base.daysOfWeekLong = gettext('Sunday Monday Tuesday Wednesday Thursday Friday Saturday').split(' ');
        base.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

        base.isLeapYear = function(year) {
            return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
        }

        base.init = function() {
            // load options
            base.options = $.extend({}, $.bmf.calendar.defaultOptions, options);

            base.container = base.$el.parent();
//          base.container.append('<div class="row" style="position: relative; z-index:5; display:hidden"><div class="col-sm-6"></div><div class="col-sm-6"></div></div>');
//          base.datefield = base.container.find('div.row div').first();
//          base.timefield = base.container.find('div.row div').last();

            base.$el.append('<span class="input-group-btn"><button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-calendar"></span></button></span>');

//          base.input = base.$el.children('input[type="text"]').first();
//
//          base.$el.find('button').first().on('click', function () {
//              base.initCalendar();
//          });
//          base.input.on('focus', function () {
//              base.initCalendar();
//          });
//          base.input.on('blur', function () {
//              window.setTimeout(function() { base.destroyCalendar(); }, 100);
//          });
        }
      
        base.getDaysInMonth = function(month, year) {
            var days;
            if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
                days = 31;
            }
            else if (month==4 || month==6 || month==9 || month==11) {
                days = 30;
            }
            else if (month==2 && base.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        };

        base.initCalendar = function() {
            base.container.children('div.row').show();
            if (base.datefield.children().length == 0) {
                base.buildDateField();
            }
            if (base.timefield.children().length == 0) {
                base.buildDateField();
            }
        }

        base.destroyCalendar = function() {
            base.container.children('div.row').hide();
        }

        base.buildTimeField = function() {
            base.timefield.html('TIME');
        }

        base.buildDateField = function() {
            $.bmf.buildcalendar(base.datefield);
        }

        // Run initializer
        base.init();
    }; // end bmf.calendar

    // default options
    $.bmf.calendar.defaultOptions = {
        href: null,
        debug: false
    };

    // register as jquery function
    $.fn.bmf_calendar = function(options){
        return $(this).find('div.input-group[data-bmf-calendar]').each(function(){
            (new $.bmf.calendar(this, options));
        });
    };
})(jQuery);


/* buildcalendar */


(function($){
    $.bmf.buildcalendar = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.buildcalendar", base);

        base.init = function(el) {
            // load options
            base.options = $.extend({}, $.bmf.calendar.defaultOptions, options);

            // initialization logic
            var table = $('<table class="table-condensed">');

            base.draw(table);
            base.destroy();
            base.$el.append(table);
        }
      
        // set strings
        base.monthsOfYear = gettext('January February March April May June July August September October November December').split(' ');
        base.daysOfWeek = gettext('Su Mo Tu We Th Fr Sa').split(' ');
        base.daysOfWeekLong = gettext('Sunday Monday Tuesday Wednesday Thursday Friday Saturday').split(' ');
        base.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

        base.isLeapYear = function(year) {
            return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
        }

        base.getDaysInMonth = function(month, year) {
            var days;
            if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
                days = 31;
            }
            else if (month==4 || month==6 || month==9 || month==11) {
                days = 30;
            }
            else if (month==2 && base.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        };

        base.destroy = function() {
            base.$el.children().remove();
        }

        base.getWeek = function(year, month, day) {
            var date = new Date(year, month-1, day - base.firstDayOfWeek);
            date.setHours(0, 0, 0, 0);
            // Thursday in current week decides the year.
            date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
            // January 4 is always in week 1.
            var week = new Date(year, 0, 4);
            // Adjust to Thursday in week 1 and count number of weeks from date to week.
            return 1 + Math.round(((date.getTime() - week.getTime()) / 86400000 - 3 + (week.getDay() + 6) % 7) / 7);
        }

        base.draw = function(el, month, year) {
            var today = new Date();
            var todayDay = today.getDate();
            var todayMonth = today.getMonth()+1;
            var todayYear = today.getFullYear();

            thead = $('<thead>');
            tbody = $('<tbody>');

            el.append(thead, tbody);

            month = parseInt(month);
            year = parseInt(year);

            if (!month) month = todayMonth;
            if (!year) year = todayYear;

            thead.append('<tr><th class="text-center">' + year + '</th><th class="text-center">&lt;</th><th colspan="5" class="text-center">' + base.monthsOfYear[month-1] + '</th><th class="text-center">&gt;</th></tr>');

            var tr = $('<tr>');
            tbody.append(tr);
            tr.append('<td>');
            for (var i = 0; i < 7; i++) {
                tr.append('<td class="text-center">'+ base.daysOfWeek[(i + base.firstDayOfWeek) % 7] +'</td>');
            }

            var startingPos = new Date(year, month-1, 1 - base.firstDayOfWeek).getDay();
            var days = base.getDaysInMonth(month, year);

            var tr = $('<tr>');
            tbody.append(tr);

            // empty days 
            for (var i = 0; i < startingPos; i++) {
                tr.append('<td class="noday"></td>');
            }

            var currentDay = 1;
            for (var i = startingPos; currentDay <= days; i++) {
                if (i%7 == 0) {
                    tr.prepend('<td class="text-center">' + base.getWeek(year, month, currentDay) + '</td>');
                }
                if (i%7 == 0 && currentDay != 1) {
                    tr = $('<tr>');
                    tbody.append(tr);
                }
                var td = $('<td class="text-center">' + currentDay +'</td>');

//              if ((currentDay==todayDay) && (month==todayMonth) && (year==todayYear)) {
//                  todayClass='today';
//              } else {
//                  todayClass='';
//              }
//
//              // use UTC function; see above for explanation.
//              if (isSelectedMonth && currentDay == selected.getUTCDate()) {
//                  if (todayClass != '') todayClass += " ";
//                  todayClass += "selected";
//              }
//
//              var cell = quickElement('td', tableRow, '', 'class', todayClass);
//
//              quickElement('a', cell, currentDay, 'href', 'javascript:void(' + callback + '('+year+','+month+','+currentDay+'));');
//
                tr.append(td);
                currentDay++;
            }
            tr.prepend('<td class="text-center">' + base.getWeek(year, month, currentDay - 1) + '</td>');
        }

        // Run initializer
        base.init();
    }; // end bmf.buildcalendar

    // default options
    $.bmf.buildcalendar.defaultOptions = {
        long_names: false,
        callback_month: null,
        callback_week: null,
        callback_day: null,
        href_year: false,
        href_month: false,
        href_week: false,
        href_day: false,
        debug: false
    };
})(jQuery);


/* buildform */
(function($){
    // register as jquery function
    $.fn.bmf_buildform = function(){
        $(this).bmf_autocomplete();
        $(this).bmf_calendar();
    };
})(jQuery);

$(document).ready(function() {
    /* Sidebar
     * ----------------------------------------------------------------------- */

    $("#sidebar p.switch a").click(function(e) {
        e.preventDefault();
        $("body").toggleClass("bmfsidebar-toggled");
    });

    /* Notification
     * ----------------------------------------------------------------------- */

    function check_notification() {
        var count = parseInt( $('#bmf_notification').data('count') );
        if (count > 0) {
            $('#bmf_notification').removeClass("new").addClass("new");
        }
    }
    check_notification();

    /* Message
     * ----------------------------------------------------------------------- */
    /*
    $('#bmf_message').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data+'</div>');
                $('#bmfmodal_logout').modal('show');
            });
        }
        else {
            $('#bmfmodal_logout').modal('show');
        }
    });
   
    /* LOGOUT
     * ----------------------------------------------------------------------- */
    $('#bmfapi_logout').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data.html+'</div>');
                $('#bmfmodal_logout').modal('show');
            });
        }
        else {
            $('#bmfmodal_logout').modal('show');
        }
    });
   
    /* SAVE VIEW
     * ----------------------------------------------------------------------- */
    $('#bmfapi_saveview').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_saveview').length == 0) {
            $('#wrap').prepend('<div class="modal fade" id="bmfmodal_saveview" tabindex="-1" role="dialog" aria-hidden="true"></div>');
        }
        var search = $(location).attr('search');
        var pathname = $(location).attr('pathname');
        var url = $(this).attr('href');
        dict = $.bmf.AJAX;
        dict.type = 'GET';
        dict.data = { search: search, pathname: pathname };
        dict.url = url;
        $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#bmfmodal_saveview').html(data.html);
                $('#bmfmodal_saveview').modal('show');
                $('#bmfmodal_saveview form').submit(function(event){
                    event.preventDefault();
                    dict = $.bmf.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serialize();
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          if (data.close == true) {
                             $('#bmfmodal_saveview .modal-body').html("TODO REFRESH PAGE");
                          }
                          else {
                             $('#bmfmodal_saveview .modal-body').html(data.html);
                          }
                      })
                      .fail(function(jqXHR, textStatus, errorThrown) {
                          console.log( errorThrown+" ("+textStatus+")" );
                      });
                });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                console.log( errorThrown+" ("+textStatus+")" );
            });
    });


    $('#bmfapi_follow').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_follow').length == 0) {
            var ct = $(this).data('ct');
            var pk = $(this).data('pk');
            var url = $(this).attr('href');
            dict = $.bmf.AJAX;
            dict.type = 'GET';
            dict.data = { ct: ct, pk: pk };
            dict.url = url;
            $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_follow" tabindex="-1" role="dialog" aria-hidden="true">'+data.html+'</div>');

                $('#bmfmodal_follow').modal('show');

                $('#bmfmodal_follow form').submit(function(event){
                    event.preventDefault();
                    dict = $.bmf.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serializeArray();
                    dict.data.push({name: 'ct', value: ct });
                    dict.data.push({name: 'pk', value: pk });
                    dict.data = $.param(dict.data);
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          $('#bmfapi_follow').removeClass('following');
                          $('#bmfapi_follow span').removeClass('glyphicon-star glyphicon-star-empty');
                          if (data.active == true) {
                            $('#bmfapi_follow').addClass('following');
                            $('#bmfapi_follow span').addClass('glyphicon-star');
                          }
                          else {
                            $('#bmfapi_follow span').addClass('glyphicon-star-empty');
                          }
                          $('#bmfmodal_follow').modal('hide');
                      })
                      .fail(function(jqXHR, textStatus, errorThrown) {
                          console.log( errorThrown+" ("+textStatus+")" );
                      });
                });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                console.log( errorThrown+" ("+textStatus+")" );
            });
        }
        else {
          $('#bmfmodal_follow').modal('show');
        }
    });
});

/*!
 * django BMF Angular UI
 */

(function() {

var BMFEVENT_ACTIVITY = "bmf.event.update.activity";
var BMFEVENT_CONTENT = "bmf.event.update.content";
var BMFEVENT_DASHBOARD = "bmf.event.update.dashboard";
var BMFEVENT_DATA = "bmf.event.update.data";
var BMFEVENT_MODAL = "bmf.event.update.modal";
var BMFEVENT_NAVIGATION = "bmf.event.update.navigation";
var BMFEVENT_OBJECT = "bmf.event.update.object";
var BMFEVENT_SIDEBAR = "bmf.event.update.sidebar";

// INIT APP
var bmfapp = angular.module('djangoBMF', []);

/*
 * ui-config
 */

bmfapp.config(['$httpProvider', '$locationProvider', '$logProvider', 'config', function($httpProvider, $locationProvider, $logProvider, config) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $locationProvider.html5Mode(true).hashPrefix('!');
    $logProvider.debugEnabled(config.debug);
}]);

bmfapp.filter('mark_safe', ['$sce', function($sce) {
    return function(value) {
        return $sce.trustAsHtml(value);
    }
}]);

// compare with https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date-and-time-formatting-specifiers
bmfapp.filter('django_strftime', [function() {
    return function(value, format) {
        var date = new Date(value);

        var dateformat_F = gettext("January February March April May June July August September October November December").split(" ");
        var dateformat_E = gettext("January February March April May June July August September October November December").split(" ");
        var dateformat_N = gettext("Jan. Feb. March April May June July August Sept. Oct. Nov. Dec.").split(" ");
        var dateformat_M = gettext("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec").split(" ");
        var dateformat_l = gettext('Sunday Monday Tuesday Wednesday Thursday Friday Saturday').split(' ');

        var fields = {
            'a': function() {
                return date.getHours() <= 12 ? gettext('a.m.') : gettext('p.m.');
            },
            'A': function() {
                return date.getHours() <= 12 ? gettext('AM') : gettext('PM');
            },
            'c': function() {
                return date.toString();
            },
            'd': function() {
                return (date.getDate() < 10) ? '0' + date.getDate() : date.getDate();
            },
            'E': function() {
                return dateformat_F[date.getMonth()];
            },
            'f': function() {
                return this.g() + ':' + this.i();
            },
            'F': function() {
                return dateformat_F[date.getMonth()];
            },
            'g': function() {
                var hours = date.getHours();
                if (hours == 0) {
                    return '12';
                }
                else {
                    return hours <= 12 ? hours : (hours - 12);
                }
            },
            'G': function() {
                return date.getHours();
            },
            'H': function() {
                return (date.getHours() < 10) ? '0' + date.getHours() : date.getHours();
            },
            'i': function() {
                return (date.getMinutes() < 10) ? '0' + date.getMinutes() : date.getMinutes();
            },
            'l': function() {
                return dateformat_l[date.getDay()];
            },
            'j': function() {
                return '' + date.getDate();
            },
            'm': function() {
                return (date.getMonth() < 9) ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
            },
            'N': function() {
                return dateformat_N[date.getMonth()];
            },
            'P': function() {
                var hours = date.getHours();
                if (date.getMinutes() == 0) {
                    if (hours == 0) return gettext('midnight');
                    if (hours == 12) return gettext('noon');
                }
                return this.f() + ' ' + this.a();
            },
            'w': function() {
                return date.getDay();
            },
            'y': function() {
                return ('' + date.getFullYear()).substr(2, 4);
            },
            'Y': function() {
                return date.getFullYear();
            },
        };
        var regex = new RegExp('[A-Za-z]');
        var result = '';
        var i = 0;
        while (i < format.length) {
            var v = format.charAt(i);
            if (regex.test(v) && v in fields) {
                result = result + fields[v]();
            }
            else {
                result = result + v;
            }
            ++i;
        }
        return result;
    }
}]);

bmfapp.filter('django_short_datetime', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("SHORT_DATETIME_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

bmfapp.filter('django_short_date', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("SHORT_DATE_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

bmfapp.filter('django_datetime', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("DATETIME_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

bmfapp.filter('django_time', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("TIME_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

bmfapp.filter('django_date', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("DATE_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

// http://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
bmfapp.filter('timesince', ['$filter', function($filter) {
    return function(value) {
        var now = new Date();
        var date = new Date(value);
        var diff = (now - date) / 1000;
        if (diff < 60) {
            return gettext('seconds ago')
        }
        diff /= 60;
        if (diff < 60) {
            return Math.floor(diff) + ' ' + gettext('minutes ago')
        }
        diff /= 60;
        if (diff < 48) {
            return Math.floor(diff) + ' ' + gettext('hours ago')
        }
        diff /= 24;
        if (diff < 31) {
            return Math.floor(diff) + ' ' + gettext('days ago')
        }
        var filter_function = $filter('django_date');
        return filter_function(value);
    }
}]);

/*
 * ui-directive
 */

bmfapp.directive('bmfLink', ['$location', '$rootScope', 'apiurl', 'appurl', 'LinkFactory', 'ModuleFromCt', function($location, $rootScope, apiurl, appurl, LinkFactory, ModuleFromCt) {
    return {
        template: '<a ng-transclude></a>',
        restrict: 'E',
        priority: 10,
        scope: false,
        replace: true,
        transclude: true,
        link: function(scope, element, attr) {
            var view = $rootScope.bmf_breadcrumbs[$rootScope.bmf_breadcrumbs.length - 1];

            var module;
            if (attr.ct) module = ModuleFromCt(attr.ct) 
            else if (scope.module) module = scope.module
            else if (view.module) module = view.module

            var pk;
            if (attr.pk) pk = attr.pk
            else if (view.kwargs.pk) pk = view.kwargs.pk

            var href = LinkFactory(attr.type, module, pk, attr.action);

            if (href) element.attr('href', href);
        },
    }
}]);

// manages links vom list views to detail views
bmfapp.directive('bmfDetail', ['LinkFactory', function(LinkFactory) {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attr) {
            element.attr(
                'href',
                LinkFactory("detail", scope.module, attr.bmfDetail, undefined)
            );

            element.on('click', function(event) {
                window.scrollTo(0,0);
            });
        }
    };
}]);


// manages form modal calls
bmfapp.directive('bmfForm', [function() {
    return {
        restrict: 'A',
        link: function(scope, element, attr) {

            element.on('click', function(event) {
                event.preventDefault();
                open_formular(this, element);
            });

            var initialize_modal = function () {
                // initialize the modal
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_edit" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"></div></div>');
                $('#bmfmodal_edit').modal({
                    keyboard: true,
                    show: false,
                    backdrop: 'static'
                });

                // delete the modals content, if closed
                $('#bmfmodal_edit').on('hidden.bs.modal', function (e) {
                    $('#bmfmodal_edit div.modal-dialog').empty();
                });

                //// reload the page if one save has appeared
                //$('#bmfmodal_edit').on('hide.bs.modal', function (e) {
                //    if ($('#bmfmodal_edit > div.page-reload').length == 1) {
                //        location.reload(false);
                //    }
                //});
            }

            var open_formular = function (clicked, element) {
                // loads the formular data into the modal
                if ($('#bmfmodal_edit').length == 0) { initialize_modal() }

                var dict = $.bmf.AJAX;
                dict.type = "GET";
                dict.url = element[0].href;
                $.ajax(dict).done(function( data, textStatus, jqXHR ) {

                    if (data.success == true && data.reload == true) {
                        // reload page without refreshing the cache
                        location.reload(false);
                        return null;
                    }

                    $('#bmfmodal_edit div.modal-dialog').prepend(data.html);
                    $('#bmfmodal_edit').modal('show');

                    // manipulate form url
                    // cause the template-tag which generates the form is not aware of the url
                    var parent_object = $('#bmfmodal_edit div.modal-dialog div:first-child');
                    var form_object = parent_object.find('form');
                    // form_object.attr('action', base.options.href.split("?",1)[0]);
                    form_object.attr('action', dict.url);
                    // apply bmf-form functions
                    form_object.bmf_buildform();

                    parent_object.find('button.bmfedit-cancel').click(function (event) {
                        // TODO check if there are multile forms and close modal or show next form
                        $('#bmfmodal_edit').modal('hide');
                    });

                    parent_object.find('button.bmfedit-submit').click(function (event) {
                        dict = $.bmf.AJAX;
                        dict.type = "POST";
                        dict.data = form_object.serialize();
                        dict.url = form_object.attr('action');
                        $.ajax(dict).done(function( data, textStatus, jqXHR ) {

                            //  # if an object is created or changed return the object's pk on success
                            //  'object_pk': 0, TODO
                            //  # on success set this to True
                            //  'success': False,
                            //  # reload page on success
                            //  'reload': False,
                            //  # OR redirect on success
                            //  'redirect': None,
                            //
                            //  # OR reload messages on success
                            //  'message': False, # TODO
                            //  # returned html
                            //  'html': None, # TODO
                            //  # return error messages
                            //  'errors': [], TODO

                            if (data.success == false) {
                                html = $($.parseHTML( data.html ));
                                form_object.html(html.find('form').html());
                                form_object.bmf_buildform();
                            }
                            else if (data.reload == true) {
                                // reload page without refreshing the cache
                                location.reload(false);
                            }
                            else if (data.redirect != null) {
                                window.location.href=data.redirect;
                            }
                            else {
                                $('#bmfmodal_edit').modal('hide');
                            }
                        });
                    });
                });
            }
        }
    };
}]);


// 
bmfapp.directive('bmfNotification', ['$http', function($http) {
    return {
        restrict: 'A',
        template: '<a ng-class="enabled ? \'btn-info\' : \'btn-default\'" title="{{ title }}"><span ng-class="symbol"></span></a>',
        replace: true,
        scope: {},
        link: function(scope, element, attr) {
            scope.enabled = scope.$eval(attr.enabled);
            scope.method = attr.bmfNotification;
            scope.url = attr.href;
            scope.symbol = "glyphicon glyphicon-question-sign";
            scope.title = "";
            if (scope.method == "new_entry") {
                scope.symbol = "glyphicon glyphicon-file";
                scope.title = gettext("New entries");
            };
            if (scope.method == "comments") {
                scope.symbol = "glyphicon glyphicon-comment";
                scope.title = gettext("New comments");
            };
            if (scope.method == "workflow") {
                scope.symbol = "glyphicon glyphicon-random";
                scope.title = gettext("Worflow changes");
            };
            if (scope.method == "files") {
                scope.symbol = "glyphicon glyphicon-paperclip";
                scope.title = gettext("New files");
            };
            if (scope.method == "detectchanges") {
                scope.symbol = "glyphicon glyphicon-edit";
                scope.title = gettext("Detected changes");
            };

            element.on('click', function(event) {
                event.preventDefault();
                var data = {};
                data[scope.method] = !scope.enabled;

                $http({
                    method: 'POST',
                    data: data,
                    url: scope.url,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                }).then(function (response) {
                    // success callback
                    // console.log("success", response);
                    scope.enabled = response.data[scope.method];
                }, function (response) {
                    // error callback
                    console.log("Notification - Error", response);
                });
            });
        },
    };
}]);


// 
bmfapp.directive('bmfTimeAgo', [function() {
    return {
        restrict: 'A',
        template: '<span title="{{ time | django_datetime }}">{{ time | timesince }}</span>',
        replace: true,
        link: function(scope, element, attr) {
            scope.time = scope.$eval(attr.bmfTimeAgo);
        }
    };
}]);


// manages the content-area
bmfapp.directive('bmfContent', ['$compile', '$rootScope', '$http', 'ApiUrlFactory', function($compile, $rootScope, $http, ApiUrlFactory) {
    return {
        restrict: 'A',
        priority: -90,
        // scope: {},
        link: function(scope, $element, attr, ctrl) {
            scope.$on(BMFEVENT_CONTENT, function(event, name) {
                update(name);
            });

            // clear all variables not in common use
            // by views
            function clear() {
                // objects primary key
                scope.pk = undefined;
                // ui informations
                scope.ui = undefined;
                // data array
                scope.data = [];

                scope.module = undefined;
                scope.pagination = undefined;
                scope.template_html = undefined;

                scope.creates = undefined;
                scope.activities = undefined;

                scope.dashboard_name = undefined;
                scope.category_name = undefined;
                scope.view_name = undefined;

                // views may define a watch on scope values, the watcher
                // stores the destroy-function which is called with the
                // cleanup
                if (scope.content_watcher != undefined) {
                    scope.content_watcher();
                }
                scope.content_watcher = undefined;
            }
            scope.template_watcher = undefined;

            // call when the view type got updated
            function update(type) {
                clear()
                if (type == "list") {
                    view_list()
                }
                if (type == "detail" || type == "detail-base") {
                    view_detail()
                }
                if (type == "notification") {
                    view_notification()
                }
            }

            function view_list(type) {
                scope.content_watcher = scope.$watch(
                    function(scope) {return scope.bmf_current_view},
                    function(newValue) {if (newValue != undefined && newValue.type == "list") upd(newValue)}
                );

                function upd(view) {
                    // update vars
                    scope.view_name = view.view.name;
                    scope.category_name = view.category.name;
                    scope.dashboard_name = view.dashboard.name;

                    // get new template
                    $http.get(view.view.api).then(function(response) {

                        var ct = response.data.ct;
                        var module = scope.$parent.bmf_modules[ct];

                        scope.creates = module.creates;
                        scope.template_html = response.data.html;

                        // get new data
                        var url = module.data + '?d=' + view.dashboard.key + '&c=' + view.category.key + '&v=' + view.view.key;

                        $http.get(url).then(function(response) {
                            scope.data = response.data.items;
                            scope.pagination = response.data.pagination;
                        });
                    });
                }
                update_html("list");
            }

            function view_detail(type) {
                scope.content_watcher = scope.$watch(
                    function(scope) {
                        if (!$rootScope.bmf_breadcrumbs || $rootScope.bmf_breadcrumbs.length == 0) {
                            return undefined
                        }
                        return $rootScope.bmf_breadcrumbs[$rootScope.bmf_breadcrumbs.length -1];
                    },
                    function(value) {if (value != undefined) upd(value)}
                );

                function upd(view) {
                    // update vars
                    scope.module = view.module;

                    // console.log(view.module);
                    scope.ui = {
                        notifications: null,
                        workflow: null,
                        views: null,
                        related: [],
                    };

                    var url = view.module.base + view.kwargs.pk  + '/';
                    $http.get(url).then(function(response) {
                        scope.ui.workflow = response.data.workflow;
                        scope.ui.views = response.data.views;
                        scope.ui.notifications = response.data.notifications;
                        scope.template_html = response.data.html

                        if (response.data.views.activity.enabled) {
                        //  var url = response.data.views.activity.url;
                        //  console.log("OLDURL", url)
                        //  $http.get(url).then(function(response) {
                        //      scope.activities = response.data;
                        //  });
                        }
                    });
                }

                update_html("detail");
            }

            function view_notification(type) {
                
                scope.content_watcher = scope.$watch(
                    function(scope) {return $rootScope.bmf_breadcrumbs[0].module},
                    function(value) {upd(value)}
                );

                scope.module = undefined;
                scope.settings = undefined;

                function upd(module) {
                    // update vars
                    scope.module = module
                    scope.settings = undefined;

                    scope.navigation = [];
                    for (var key in $rootScope.bmf_modules) {
                        var data = $rootScope.bmf_modules[key];
                        data.count = 0;
                        scope.navigation.push(data);
                    };

                    var url = ApiUrlFactory(null, 'notification', 'count');
                    $http.get(url).then(function(response) {
                        for (var i in scope.navigation) {
                            if (scope.navigation[i].ct in response.data.data) {
                                scope.navigation[i].count = response.data.data[scope.navigation[i].ct];
                            }
                        };
                    });

                    if (module) {
                        var url = ApiUrlFactory(module, 'notification', 'list');
                        $http.get(url).then(function(response) {
                            scope.data = response.data.items;
                        });

                        var url = ApiUrlFactory(module, 'notification', 'view');
                        $http.get(url).then(function(response) {
                            scope.settings = response.data;
                            scope.settings.api = url;
                        });
                    }
                }
                update_html("notification");
            }

            function update_html(type) {
                $element.html($rootScope.bmf_templates[type]).show();
                $compile($element.contents())(scope);
            }
        }
    };
}]);


// compiles the content of a scope variable
bmfapp.directive('bmfTemplate', ['$compile', function($compile) {
    return {
        restrict: 'E',
        priority: -80,
        link: function(scope, $element) {

            if (scope.$parent.template_watcher != undefined) {
                scope.$parent.template_watcher();
            }

            scope.$parent.template_watcher = scope.$watch(
                function(scope) {return scope.template_html},
                function(newValue) {
                    if (newValue != undefined) {
                        $element.html(newValue).show();
                        $compile($element.contents())(scope);
                    }
                }
            );
        }
    };
}]);


bmfapp.directive('bmfSiteRelated', [function() {
    return {
        restrict: 'C',
        scope: {
        },
        template: function(tElement, tAttrs) {
            return tElement.html();
        },
        controller: ['$scope', '$location', '$http', 'ApiUrlFactory', 'ModuleFromUrl', function($scope, $location, $http, ApiUrlFactory, ModuleFromUrl) {

            $scope.scopename = "related";

            $scope.visible = false;
            $scope.parent_module = null;
            $scope.module = null;
            $scope.pk = null;

            $scope.urlparam = undefined;
            $scope.paginator = undefined;

            function clear_data() {
                $scope.data = [];
                $scope.errors = [];
            }
            clear_data();

            function set_dataurl() {
                var search = $location.search();
                $scope.urlparam = search.open;

                if ($scope.urlparam) {
                    $scope.dataurl = ApiUrlFactory(
                        $scope.parent_module,
                        'related',
                        $scope.urlparam,
                        $scope.pk
                    ) + '?page=' + (search.rpage || 1);
                }
            }

            $scope.$watch(function(scope) {return scope.dataurl}, get_data);

            function get_data(url) {
                clear_data();
                if (!url) return false;
                $http.get(url).then(function(response) {
                    $scope.module = ModuleFromUrl(response.data.model.app_label, response.data.model.model_name);
                    $scope.data = response.data.items;
                    $scope.template_html = response.data.html;
                    $scope.paginator = response.data.paginator;
                });
            }

            $scope.open = function(slug) {
                if (slug == $scope.urlparam) {
                    $scope.urlparam = undefined;
                }
                else {
                    $scope.urlparam = slug;
                }
                // changing the location will result in firing the event
                // which reloads the data
                $location.search('open', $scope.urlparam);
            }

            $scope.$on(BMFEVENT_OBJECT, function(event, module, pk) {
                if (module && pk) {
                    $scope.visible = true;
                    $scope.parent_module = module;
                    // $scope.module = module;
                    $scope.pk = pk;
                    set_dataurl();
                }
                else $scope.visible = false;
            });
        }],
        link: function(scope, $element) {
            scope.$watch(
                function(scope) {return scope.visible},
                function(value) {
                    if (value) {
                        $element.show();
                    }
                    else {
                        $element.hide();
                    }
                }
            );

        },
    };
}]);


bmfapp.directive('bmfSiteActivity', [function() {
    return {
        restrict: 'C',
        scope: {},
        template: function(tElement, tAttrs) {
            return tElement.html();
        },
        controller: ['$scope', '$location', '$http', 'ApiUrlFactory', function($scope, $location, $http, ApiUrlFactory) {

            $scope.scopename = "activity";

            // TODO event to update activity
            // TODO add timer fire update event every two minutes

            $scope.visible = false;
            $scope.module = null;
            $scope.pk = null;

            function clear_data() {
                $scope.formdata = {};
                $scope.data = [];
                $scope.errors = [];
                $scope.notification = undefined;
                $scope.paginator = undefined;
            }
            clear_data();

            function set_dataurl() {
                var search = $location.search();
                $scope.notifyurl = ApiUrlFactory(
                    $scope.module,
                    'notification',
                    'view',
                    $scope.pk
                );
                $scope.dataurl = ApiUrlFactory(
                    $scope.module,
                    'activity',
                    undefined,
                    $scope.pk
                ) + '?page=' + (search.apage || 1);
            }
            $scope.$watch(function(scope) {return scope.dataurl}, get_data);
  
            function get_data(url) {
                clear_data();
                if (!url) return false;
                $http.get(url).then(function(response) {
                    $scope.data = response.data.items;
                    $scope.notification = response.data.notification;
                    $scope.paginator = response.data.paginator;
                });
            }

            $scope.processForm = function() {
                var url = ApiUrlFactory(
                    $scope.module,
                    'activity',
                    undefined,
                    $scope.pk
                );

                $http({
                    method: 'POST',
                    data: $scope.formdata,
                    url: url,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                }).then(function (response) {
                    // success callback
                    // console.log("success", this, response);
                    get_data($scope.dataurl);
                }, function (response) {
                    // error callback
                    console.log("ActivityForm - Error", response);
                    alert(response.data.non_field_errors[0]);
                });
            }

            $scope.$on(BMFEVENT_OBJECT, function(event, module, pk) {
                if (module && pk) {
                    $scope.visible = true;
                    $scope.module = module;
                    $scope.pk = pk;
                    set_dataurl();
                }
                else $scope.visible = false;
            });
        }],
        link: function(scope, $element) {
            scope.$watch(
                function(scope) {return scope.visible},
                function(value) {
                    if (value) {
                        $element.show();
                    }
                    else {
                        $element.hide();
                    }
                }
            );

        },
    };
}]);


bmfapp.directive('bmfSiteTemplate', ['$compile', function($compile) {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, $element) {
            scope.$watch(
                function(scope) {return scope.template_html},
                function(value) {
                    $element.hide()
                    $element.html(value || '');
                    $compile($element.contents())(scope);
                    $element.show();
                }
            );
        }
    };
}]);


bmfapp.directive('bmfSiteContent', [function() {
    return {
        restrict: 'C',
        scope: {},
        template: function(tElement, tAttrs) {
            return tElement.html();
        },
        controller: ['$scope', '$location', '$http', 'ApiUrlFactory', 'ModuleFromUrl', function($scope, $location, $http, ApiUrlFactory, ModuleFromUrl) {

            $scope.scopename = "content";
            $scope.visible = false;

        //  $scope.parent_module = null;
        //  $scope.module = null;
        //  $scope.pk = null;

        //  $scope.urlparam = undefined;
        //  $scope.paginator = undefined;

        //  function clear_data() {
        //      $scope.data = [];
        //      $scope.errors = [];
        //  }
        //  clear_data();

        //  function set_dataurl() {
        //      var search = $location.search();
        //      $scope.urlparam = search.open;

        //      if ($scope.urlparam) {
        //          $scope.dataurl = ApiUrlFactory(
        //              $scope.parent_module,
        //              'related',
        //              $scope.urlparam,
        //              $scope.pk
        //          ) + '?page=' + (search.rpage || 1);
        //      }
        //  }

        //  $scope.$watch(function(scope) {return scope.dataurl}, get_data);

        //  function get_data(url) {
        //      clear_data();
        //      if (!url) return false;
        //      $http.get(url).then(function(response) {
        //          $scope.module = ModuleFromUrl(response.data.model.app_label, response.data.model.model_name);
        //          $scope.data = response.data.items;
        //          $scope.template_html = response.data.html;
        //          $scope.paginator = response.data.paginator;
        //      });
        //  }

        //  $scope.open = function(slug) {
        //      if (slug == $scope.urlparam) {
        //          $scope.urlparam = undefined;
        //      }
        //      else {
        //          $scope.urlparam = slug;
        //      }
        //      // changing the location will result in firing the event
        //      // which reloads the data
        //      $location.search('open', $scope.urlparam);
        //  }

        //  $scope.$on(BMFEVENT_OBJECT, function(event, module, pk) {
        //      if (module && pk) {
        //          $scope.visible = true;
        //          $scope.parent_module = module;
        //          // $scope.module = module;
        //          $scope.pk = pk;
        //          set_dataurl();
        //      }
        //      else $scope.visible = false;
        //  });
        }],
        link: function(scope, $element) {
          //scope.$watch(
          //    function(scope) {return scope.visible},
          //    function(value) {
          //        if (value) {
          //            $element.show();
          //        }
          //        else {
          //            $element.hide();
          //        }
          //    }
          //);
        },
    };
}]);

/*
 * ui-factory
 */

// This factory uses the rootScope to generate a from a given type (req),
// action(opt) and primary_key(opt)
bmfapp.factory('ApiUrlFactory', ['$rootScope', function($rootScope) {
    return function(module, type, action, pk) {
        if (!$rootScope.bmf_api.base) throw "api not loaded";
        if (!type) throw "no type defined";
        var url = $rootScope.bmf_api.base + type + '/';
        if (module) url += module.app + '/' + module.model + '/';
        if (action) url += action + '/';
        if (pk) url += pk + '/';
        return url
    }
}]);

// This factory uses the rootScope to generate a from a given type (req),
// action(opt) and primary_key(opt)
bmfapp.factory('LinkFactory', ['$location', '$rootScope', 'apiurl', 'appurl', 'ModuleFromCt', function($location, $rootScope, apiurl, appurl, ModuleFromCt) {
    return function(type, module, pk, action) {
        var view = $rootScope.bmf_breadcrumbs[$rootScope.bmf_breadcrumbs.length - 1];
        if (!module && view.module) module = view.module;
        var url;

        if (type == "create" && action && module) {
            url = apiurl + 'module/' + module.ct + '/' + type + '/' + action + '/';
        }

        if (type == "detail" && module && pk) {
            if (view && view.name in ["notification", "list"]) {
                url = $location.path() + pk + '/';
            }
            else {
                url = appurl + 'detail/' + module.app + '/' + module.model + '/' + pk + '/';
            }
        }

        return url
    }
}]);


/**
 * @description
 *
 * Get the dashboard from url parameters
 *
 */
bmfapp.factory('ViewFromUrl', ['$rootScope', function($rootScope) {
    return function(dashboard, category, view) {
        var data = undefined
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            if (d.key == dashboard) d.categories.forEach(function(c, ci) {
                if (c.key == category) c.views.forEach(function(v, vi) {
                    if (v.key == view) {
                        data = {
                            view: v,
                            category: c,
                            dashboard: d,
                        }
                    }
                });
            });
        });
        return data
    }
}]);


/**
 * @description
 *
 * Get the module from url parameters
 *
 */
bmfapp.factory('ModuleFromUrl', ['$rootScope', function($rootScope) {
    return function(app_label, model_name) {
        var data = undefined
        for (var key in $rootScope.bmf_modules) {
            if ($rootScope.bmf_modules[key].app == app_label && $rootScope.bmf_modules[key].model == model_name ) return data = $rootScope.bmf_modules[key];
        };
        return data
    }
}]);


/**
 * @description
 *
 * Get the module from a content-type
 *
 */
bmfapp.factory('ModuleFromCt', ['$rootScope', function($rootScope) {
    return function(ct) {
        return $rootScope.bmf_modules[ct];
    }
}]);


/**
 * @description
 *
 * Parse the url, validate and update rootScope
 *
 */
bmfapp.factory('ViewUrlconf', ['$rootScope', 'ViewFromUrl', 'ModuleFromCt', 'ModuleFromUrl', function($rootScope, ViewFromUrl, ModuleFromCt, ModuleFromUrl) {
    return function(url) {
        // break if api is not loaded
        if (!$rootScope.bmf_dashboards || !$rootScope.bmf_modules) return false;

        // https://gist.github.com/jlong/2428561
        var parser = document.createElement('a');
        parser.href = url;

        var urlconf = undefined
        $rootScope.bmf_view_urlconf.forEach(function(view, i) {
            if (view.regex.test(parser.pathname)) urlconf = view;
        });

        if (!urlconf) return false;

        var exp = urlconf.regex.exec(parser.pathname);
        var kwargs = {};
        var kwargs_parent = {};
        urlconf.args.forEach(function(arg, i) {
            kwargs[arg] = exp[i+1];
            if (arg != 'pk') kwargs_parent[arg] = exp[i+1];
        });

        // Validation
        var view = undefined;
        var module = undefined;
        if ('app_label' in kwargs && 'model_name' in kwargs) {
            module = ModuleFromUrl(kwargs.app_label, kwargs.model_name);
            if (module == undefined) return false;
            $rootScope.bmf_module = module;
        }
        else if ('dashboard' in kwargs && 'category' in kwargs && 'view' in kwargs) {
            view = ViewFromUrl(kwargs.dashboard, kwargs.category, kwargs.view);
            if (view == undefined) return false;

            $rootScope.bmf_last_dashboard = {
                key: view.dashboard.key,
                name: view.dashboard.name
            };
            $rootScope.bmf_last_view = view;

            module = ModuleFromCt(view.view.ct);
            if (module == undefined) return false;
            $rootScope.bmf_module = module;

            // TODO REMOVE ME
            if ('pk' in kwargs == false) {
                $rootScope.bmf_current_view = {
                    type: urlconf.name,
                    view: view.view,
                    category: view.category,
                    dashboard: view.dashboard,
                };
            }
        }

        // Fire event to update content layer
        // (needs to be fired before breadcrumbs are updated)
        $rootScope.bmfevent_content(urlconf.name);

        // Overwrite the breadcrumbs
        if (urlconf.parent == null) {
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            }];
        }
        // Update the breadcrumbs if they are not defined
        else if ($rootScope.bmf_breadcrumbs.length == 0) {
            var regex = new RegExp('^(.*/)[0-9]+/$');
            $rootScope.bmf_breadcrumbs = [{
                name: urlconf.parent,
                module: module || null,
                url: regex.exec(parser.pathname)[1],
                kwargs: kwargs_parent,
            },{
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            }];
        }
        else {
            // Walk over each breadcrumb until the path is matched
            // return matched path with updated url or append a new entry
            var index = undefined;
            $rootScope.bmf_breadcrumbs.forEach(function(crumb, i) {
                if (crumb.url == url) index = i;
            });
            if (index) for (var i=($rootScope.bmf_breadcrumbs.length - 1); i>index; i--) {
                delete $rootScope.bmf_breadcrumbs[i];
            }

            $rootScope.bmf_breadcrumbs.push({
                name: urlconf.name,
                module: module || null,
                url: url,
                kwargs: kwargs,
            });
        }

        // fire events (with updated breadcrumbs)
        if (view) $rootScope.bmfevent_dashboard(kwargs.dashboard);
        $rootScope.bmfevent_object(module || null, kwargs.pk || null);

        return true
    }
}]);

/*
 * ui-controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
bmfapp.controller('FrameworkCtrl', ['$http', '$rootScope', '$scope', '$window', '$log', 'config', function($http, $rootScope, $scope, $window, $log, config) {

    /**
     * @description
     *
     * This scope stores the base url to the API (needed for lookups)
     *
     */
    $rootScope.bmf_api_base = angular.element.find('body')[0].dataset.api;

    /**
     * @description
     *
     * This scope stores the base url to the APP (needed for lookups)
     *
     */
    $rootScope.bmf_app_base = angular.element.find('body')[0].dataset.app;

    /**
     * @description
     *
     * This scope stores the currently active module
     *
     */
    $rootScope.bmf_module = undefined;

    /**
     * @description
     *
     * Every overlay get appended to this list. we only show one modal
     * per time and update the content as long as this list is not empty
     *
     * data
     * - TODO??
     *
     */
    $rootScope.bmf_modal = [];

    /**
     * @description
     *
     * The breadcrumbs are filled with data as the user navigates through the
     * framework. it contains information about the history to provide the
     * functionality to go back one page. With this we are able to travel
     * from a module to another without changing the overlaying view.
     * 
     * The listing pages overwrite this, while every detail-page appends to
     * this.
     *
     * data is generated via the ViewUrlconf factory
     * - name: the view callback name
     * - url: the called url
     * - kwargs: the views keyword arguments
     *
     */
    $rootScope.bmf_breadcrumbs = [];

    /**
     * @description
     *
     * The urlconf is needed to map an url to a view / controller (?)
     * TODO: check if if could be loaded via the REST-API
     *
     */
    $rootScope.bmf_view_urlconf = [
        {
            name: 'list',
            parent: null,
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/$'),
            args: ['dashboard', 'category', 'view'],
        },
        {
            name: 'detail-base',
            parent: 'list',
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['dashboard', 'category', 'view', 'pk'],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/$'),
            args: [],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/$'),
            args: ['app_label', 'model_name'],
        },
        {
            name: 'detail-base',
            parent: 'notification',
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['app_label', 'model_name', 'pk'],
        },
        {
            name: 'detail',
            parent: undefined,
            regex: new RegExp('detail/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['app_label', 'model_name', 'pk'],
        },
    ];
    // TODO this is currenty unused
    $rootScope.bmf_api_urlconf = [
    ];

    /**
     * @description
     *
     * Event broadcaster
     *
     */
    $rootScope.bmfevent_activity = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_ACTIVITY);
    }
    $rootScope.bmfevent_content = function(name) {
        var crumbs = $rootScope.bmf_breadcrumbs;
        if (!crumbs || crumbs.length == 0 || crumbs[crumbs.length - 1].name != name) {
            $rootScope.$broadcast(BMFEVENT_CONTENT, name)
        }
    }
    $rootScope.bmfevent_dashboard = function(key) {
        $log.debug(BMFEVENT_DASHBOARD, key)
        $rootScope.$broadcast(BMFEVENT_DASHBOARD, key);
    }
    $rootScope.bmfevent_data = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_DATA);
    }
    $rootScope.bmfevent_modal = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_MODAL);
    }
    $rootScope.bmfevent_navigation = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_NAVIGATION);
    }
    $rootScope.bmfevent_object = function(module, pk) {
        $rootScope.$broadcast(BMFEVENT_OBJECT, module, pk);
    }

    $rootScope.bmfevent_sidebar = function(dashboard_key) {
        $rootScope.bmf_dashboards.forEach(function(d, i) {
            if (d.key == dashboard_key) {
                $rootScope.$broadcast(BMFEVENT_SIDEBAR, d.key, d.name);
            }
        });
    }

    // pace to store basic templates
    /**
     * @description
     *
     * place where all templates are stored
     *
     */
    $rootScope.bmf_templates = {
        'list': '',
        'detail': '',
        'notification': '',
    };


    $rootScope.bmf_api = {
        base: angular.element.find('body')[0].dataset.api,
        app_label: undefined,
        model_name: undefined,
        module: undefined,
    };

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all top navigation
    $rootScope.bmf_navigation = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    $rootScope.bmf_modules = undefined;

    $rootScope.bmf_ui = undefined;

    $rootScope.bmf_last_dashboard = undefined;
    $rootScope.bmf_last_view = undefined;

    // Update sidebar and Dashboard objects
    var sidebar = {}
    config.dashboards.forEach(function(element, index) {
        sidebar[element.key] = element.categories;
    });

    var modules = {}
    config.modules.forEach(function(element, index) {
        modules[element.ct] = element;
    });

    $rootScope.bmf_modules = modules;
    $rootScope.bmf_sidebars = sidebar;

    $rootScope.bmf_ui = config.ui;
    $rootScope.bmf_dashboards = config.dashboards;
    $rootScope.bmf_templates = config.templates;
    $rootScope.bmf_navigation = config.navigation;
}]);


// bmfapp.controller('ModalCtrl', [function() {
// }]);


// This controller updates the dashboard dropdown menu
bmfapp.controller('SidebarCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
    $scope.$on(BMFEVENT_SIDEBAR, function(event, key, name) {update(key, name)});

    $scope.data = [];

    function update(key, name) {
        var root = $rootScope.bmf_breadcrumbs[0];
        dashboard(root, key, name);
    }

    function dashboard(root, key, name) {
        var data = []
        data.push({
            'class': 'sidebar-board',
            'name': name,
        });

        $rootScope.bmf_sidebars[key].forEach(function(c, ci) {
            data.push({'name': c.name});
            c.views.forEach(function(v, vi) {
                if (root && 'dashboard' in root.kwargs && 'category' in root.kwargs && 'view' in root.kwargs && root.kwargs.dashboard == key && root.kwargs.category == c.key && root.kwargs.view == v.key) {
                    data.push({'name': v.name, 'url': v.url, 'class': 'active'});
                }
                else {
                    data.push({'name': v.name, 'url': v.url});
                }
            });
        });
        $scope.data = data;
    }
}]);


// This controller updates the dashboard dropdown menu
bmfapp.controller('DashboardCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {

    $scope.$on(BMFEVENT_DASHBOARD, function(event, key) {update(key)});

    function update(key) {
        var response = [];
        var data = [];
        var current = undefined;

        $rootScope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (key == d.key) {
                active = true;
                current = d;
            }
            data.push({
                'key': d.key,
                'name': d.name,
                'active': active,
            });
        });

        // fire event
        if (current) {
            $rootScope.bmfevent_sidebar(key);
        }

        $scope.data = data;
        $scope.current = current;
    }
    update();

    $scope.update = update;
}]);


// This controller updates the dashboards navigation
bmfapp.controller('NavigationCtrl', ['$scope', '$interval', '$http', function($scope, $interval, $http) {
    $scope.data = undefined;

    $scope.$watch(
        function(scope) {return scope.bmf_navigation && scope.bmf_navigation.length || 0},
        function(newValue) {if (newValue != undefined) init_navigation()}
    );

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        $scope.data.forEach(function(nav, i) {
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
        });
    });

    function init_navigation() {
        if (!$scope.bmf_navigation) return false;

        $scope.data = $scope.bmf_navigation;

        $scope.update = function (i) {
            nav = $scope.data[i];
            // console.log("TIMER", i, nav)
            $http({
                method: 'GET',
                url: nav.api,
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                // success callback
                // console.log("success", this, response);
                $scope.data[i].active = response.data.active;
                $scope.data[i].count = response.data.count;
            }, function (response) {
                // error callback
                console.log("Navigation Timer Error", response);
            });
        }

        $scope.data.forEach(function(nav, i) {
            // use the button as a link if url is set
            if (nav.url == undefined) nav.url = '#';

            // stop an old timer
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
            nav.timer = undefined;
            nav.active = false;
            nav.count = 0;

            if (nav.api && nav.intervall) {
                $scope.update(i);
                nav.timer = $interval(function() {
                    $scope.update(i)
                }, nav.intervall * 1000);
            }
        });
    }
}]);


// bmfapp.controller('ContentCtrl', [function() {
// }]);


// bmfapp.controller('DataCtrl', [function() {
// }]);


// bmfapp.controller('PaginationCtrl', [function() {
// }]);


bmfapp.controller('ActivityCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.data = {};
    $scope.processForm = function() {
        var url = $scope.$parent.$parent.ui.views.activity.url;

        $http({
            method: 'POST',
            data: $scope.data,
            url: url,
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
            // success callback
            // console.log("success", this, response);
            window.location.reload(); 
        }, function (response) {
            // error callback
            console.log("ActivityForm - Error", response);
            alert(response.data.non_field_errors[0]);
        });
    }
}]);


/*
 * View specific controller
 */


// bmfapp.controller('ListViewCtrl', [function() {
// }]);


// bmfapp.controller('DetailViewCtrl', [function() {
// }]);


// bmfapp.controller('NotificationViewCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
// }]);

/*
 * ui-run
 */


bmfapp.run(['$rootScope', '$location', '$window', 'ViewUrlconf', function($rootScope, $location, $window, ViewUrlconf) {
    $rootScope.$on('$locationChangeStart', function(event, next, current) {
        if (!ViewUrlconf(next)) {
            // if the url is not managed by the framework, prevent default
            // action from the angularJS url management and redirect browser to the new url
            // if the url was changed
            event.preventDefault(true);
            if (next != current) {
                $window.location = next;
            }
        }
    });
}]);

(function() {
    var injector = angular.injector(["ng"]);
    var $http = injector.get("$http");
    var apiurl = angular.element.find('body')[0].dataset.api;
    var appurl = angular.element.find('body')[0].dataset.app;

    bmfapp.constant("apiurl", apiurl);
    bmfapp.constant("appurl", appurl);

    $http.get(apiurl).then(function(response){
        bmfapp.constant("config", response.data);

        if (response.data.debug) {
            console.debug("BMF-API", response.data);
        }

        angular.element(document).ready(function() {
            // bootstrap angular
            angular.bootstrap(document, ["djangoBMF"]);
        });
    }, function(response){
        // error handling
        console.error(response);
        alert(gettext('Error!\nCould not load the Application'));
    });
}());

}()); // close ui definition
