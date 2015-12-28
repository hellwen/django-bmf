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

// Event send, when the activity list needs to be reloaded
var BMFEVENT_ACTIVITY = "bmf.event.activity";

// Event send, when the model details need to be updated
var BMFEVENT_MODELDETAIL = "bmf.event.modeldetail";

// Event send, when the model details need to be updated
var BMFEVENT_MODELLIST = "bmf.event.modellist";

// INIT APP
var app = angular.module('djangoBMF', []);

/*
 * ui-config
 */

app.config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $locationProvider.html5Mode(true).hashPrefix('!');
}]);

app.filter('mark_safe', ['$sce', function($sce) {
    return function(value) {
        return $sce.trustAsHtml(value);
    }
}]);

// compare with https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date-and-time-formatting-specifiers
app.filter('django_strftime', [function() {
    return function(value, format) {
        var date = new Date(value);

        var dateformat_F = gettext("January February March April May June July August September October November December").split(" ");
        var dateformat_N = gettext("Jan. Feb. March April May June July August Sept. Oct. Nov. Dec.").split(" ");

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
                    return hours <= 12 ? '' + hours : '' + (hours - 12);
                }
            },
            'H': function() {
                return (date.getHours() < 10) ? '0' + date.getHours() : date.getHours();
            },
            'i': function() {
                return (date.getMinutes() < 10) ? '0' + date.getMinutes() : date.getMinutes();
            },
            'j': function() {
                return '' + date.getDate();
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
                return '' + date.getDay();
            },
            'y': function() {
                return ('' + date.getFullYear()).substr(2, 4);
            },
            'Y': function() {
                return '' + date.getFullYear();
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

app.filter('django_datetime', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("DATETIME_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

app.filter('django_time', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("TIME_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

app.filter('django_date', ['$filter', function($filter) {
    var filter_function = $filter('django_strftime');
    var format = get_format("DATE_FORMAT");
    return function(value) {
        return filter_function(value, format);
    }
}]);

/*
 * ui-directive
 */

// manages form modal calls
app.directive('bmfForm', [function() {
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


// manages links vom list views to detail views
app.directive('bmfDetail', ["$location", function($location) {
    return {
        restrict: 'A',
        link: function(scope, element, attr) {
            element.on('click', function(event) {
                var next = $location.path() + attr.bmfDetail + '/';
                $location.path(next);
                window.scrollTo(0,0);
            });
        }
    };
}]);


// 
app.directive('bmfTimeAgo', [function() {
    return {
        restrict: 'A',
        template: '<span title="{{ time | django_datetime }}">{{ time | django_datetime }}</span>',
        replace: true,
        link: function(scope, element, attr) {
            scope.time = scope.$eval(attr.bmfTimeAgo);
            // var d = new Date(scope.$eval(attr.bmfTimeAgo));
            // scope.timeago = d.strftime(get_format("DATETIME_INPUT_FORMATS")[0]);
        }
    };
}]);


// manages the content-area
app.directive('bmfContent', ['$compile', '$http', function($compile, $http) {
    return {
        restrict: 'A',
        priority: -90,
        link: function(scope, $element) {
            scope.$watch(
                function(scope) {
                    if (scope.bmf_current_view) {
                        return scope.bmf_current_view.type
                    }
                    return undefined
                },
                function(newValue) {if (newValue != undefined) update(newValue)}
            );

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
                if (type == "detail") {
                    view_detail()
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
                    function(scope) {return scope.bmf_current_view},
                    function(newValue) {if (newValue != undefined && newValue.type == "detail") upd(newValue)}
                );

                function upd(view) {
                    // update vars
                    scope.view_name = view.view.name;
                    scope.category_name = view.category.name;
                    scope.dashboard_name = view.dashboard.name;
                    scope.module = view.module;

                    scope.ui = {
                        workflow: null,
                        views: null,
                    };

                    var url = view.module.base + view.pk  + '/';
                    $http.get(url).then(function(response) {
                        scope.ui.workflow = response.data.workflow;
                        scope.ui.views = response.data.views;
                        scope.template_html = response.data.html

                        if (response.data.views.activity.enabled) {
                            var url = response.data.views.activity.url;
                            $http.get(url).then(function(response) {
                                scope.activities = response.data;
                                console.log(response.data);
                            });
                        }
                    });
                }

                update_html("detail");
            }

            function update_html(type) {
                $element.html(scope.bmf_templates[type]).show();
                $compile($element.contents())(scope);
            }
        }
    };
}]);


// compiles the content of a scope variable
app.directive('bmfTemplate', ['$compile', function($compile) {
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

/*
 * ui-factory
 */

app.factory('CurrentView', ['$rootScope', '$location', 'PageTitle', function($rootScope, $location, PageTitle) {
    function go(next) {
        $rootScope.bmf_current_view = next;
        if (next && ["list", "detail"].indexOf(next.type) >= 0) {
            PageTitle.set(next.dashboard.name + ' - ' + next.category.name + ' - ' + next.view.name);
            $rootScope.bmf_current_dashboard = {
                key: next.dashboard.key,
                name: next.dashboard.name
            };
        }
    }

    function update(url, prefix) {
        var current = get(url, prefix);
        go(current);
        return current
    }

    function get(url, prefix) {
        if (url == undefined) {
            url = $location.path();
        }
        if (prefix) {
            if ($location.protocol() == 'http' && $location.port() == 80) {
                prefix = 'http://'+ $location.host();
            }
            else if ($location.protocol() == 'https' && $location.port() == 443) {
                prefix = 'https://'+ $location.host();
            }
            else {
                prefix = $location.protocol() + '://' + $location.host() + ':' + $location.port()
            }
        }
        else {
            prefix = ''
        }
        var current = undefined;

        // LIST AND DETAIL
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            d.categories.forEach(function(c, ci) {
                c.views.forEach(function(v, vi) {
                    var regex = new RegExp('^' + prefix + v.url + '([0-9]+)/$');

                    // check if the view relates to a list view
                    if (prefix + v.url == url) {
                        current = {
                            type: 'list',
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }

                    // check if the view relates to a detail view
                    if (regex.test(url)) {
                        current = {
                            type: 'detail',
                            module: $rootScope.bmf_modules[v.ct],
                            pk: regex.exec(url)[1],
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }
                });
            });
        });
        if (current) {
            return current;
        }
    }
    return {get: get, go: go, update: update}
}]);

app.factory('PageTitle', function() {
    var title = '';
    return {
        get: function() { return title; },
        set: function(newTitle) { title = newTitle }
    };
});

/*
 * ui-controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
app.controller('FrameworkCtrl', ['$http', '$rootScope', '$scope', '$window', 'CurrentView', 'PageTitle', function($http, $rootScope, $scope, $window, CurrentView, PageTitle) {

    // pace to store basic templates
    $rootScope.bmf_templates = {
        // template used to display items from the data api as a list
        'list': '',
        'detail': '',
    };

    // place to store all dashboards
    $rootScope.PageTitle = PageTitle;

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all top navigation
    $rootScope.bmf_navigation = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    // place to store all sitemaps
    $rootScope.bmf_modules = undefined;

    // holds the current dashboard
    $rootScope.bmf_current_dashboard = undefined;

    // holds all informations about the current view
    $rootScope.bmf_current_view = undefined

    // data holder
    $rootScope.bmf_data = undefined;

    // Load data from REST API
    var url = angular.element.find('body')[0].dataset.api;
    $http.get(url).then(function(response) {

        // Update sidebar and Dashboard objects
        var sidebar = {}
        response.data.dashboards.forEach(function(element, index) {
            sidebar[element.key] = element.categories;
        });

        var modules = {}
        response.data.modules.forEach(function(element, index) {
            modules[element.ct] = element;
        });

        $rootScope.bmf_modules = modules;
        $rootScope.bmf_sidebars = sidebar;

        $rootScope.bmf_dashboards = response.data.dashboards;
        $rootScope.bmf_debug = response.data.debug;
        $rootScope.bmf_templates = response.data.templates;
        $rootScope.bmf_navigation = response.data.navigation;

        if (response.data.debug) {
            console.log("BMF-API", response.data);
        }

        CurrentView.update();
    });

    $scope.$on('$locationChangeStart', function(event, next, current) {
        // only invoke if dashboards are present (and the ui is loaded propperly)
        if ($rootScope.bmf_dashboards) {
            var next_view = CurrentView.get(next, true);
            if (next_view) {
                CurrentView.go(next_view);
                return true
            };
        }

        // Case when the target url is not managed by the ui
        event.preventDefault(true);
        if (next != current) {
            $window.location = next;
        }
    });
}]);

// This controller updates the dashboard dropdown menu
app.controller('DashboardCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {

    $scope.data = [];
    $scope.current_dashboard = null;

    $scope.$watch(
        function(scope) {return scope.bmf_dashboards},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );
    $scope.$watch(
        function(scope) {return scope.bmf_current_dashboard},
        function(newValue) {if (newValue != undefined) update_dashboard()}
    );

    function update_dashboard(key) {
        var response = [];
        var current_dashboard = [];
        var current = $scope.bmf_current_dashboard;

        $scope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (current && current.key == d.key || key && key == d.key) {
                active = true
            }

            response.push({
                'key': d.key,
                'name': d.name,
                'active': active,
            });
        });

        $scope.data = response;
        $scope.current_dashboard = $scope.bmf_current_dashboard;
    }

    $scope.update = function(key) {
        var name;
        $scope.bmf_dashboards.forEach(function(d, di) {
            if (key && key == d.key) {
                name = d.name;
            }
        });

        if (name) {
            $rootScope.bmf_current_dashboard = {
                key: key,
                name: name
            };
        }
        else {
            $rootScope.bmf_current_dashboard = undefined;
        }
    };

}]);

// This controller updates the dashboard dropdown menu
app.controller('SidebarCtrl', ['$scope', function($scope) {
    $scope.data = [];

    $scope.$watch(
        function(scope) {return scope.bmf_current_view},
        function(newValue) {if (newValue != undefined && (newValue.type == "list" || newValue.type == "detail")) update_sidebar()}
    );
    $scope.$watch(
        function(scope) {return scope.bmf_current_dashboard},
        function(newValue) {if (newValue != undefined) update_sidebar()}
    );

    function update_sidebar() {
        var response = [];
        var key = $scope.bmf_current_dashboard.key;

        response.push({
            'class': 'sidebar-board',
            'name': $scope.bmf_current_dashboard.name
        });

        $scope.bmf_sidebars[key].forEach(function(c, ci) {
            response.push({'name': c.name});
            c.views.forEach(function(v, vi) {
                if ($scope.bmf_current_view && ($scope.bmf_current_view.type == "list" || $scope.bmf_current_view.type == "detail") && c.key == $scope.bmf_current_view.category.key && v.key == $scope.bmf_current_view.view.key) {
                    response.push({'name': v.name, 'url': v.url, 'class': 'active'});
                }
                else {
                    response.push({'name': v.name, 'url': v.url});
                }
            });
        });

        $scope.data = response;
    }
}]);

// This controller manages the activity form
app.controller('ActivityFormCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.data = {};
    console.log($scope);
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
        })
    }
}]);


// This controller updates the dashboards navigation
app.controller('NavigationCtrl', ['$scope', '$interval', function($scope, $interval) {
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
            nav = $scope.data[i]
            console.log("TIMER", i, nav)
        }

        $scope.data.forEach(function(nav, i) {
            // use the button as a link if url is set
            if (nav.url == undefined) nav.url = '#';

            // stop an old timer
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
            nav.timer = undefined;

            if (nav.api && nav.intervall) {
                $scope.update(i);
                nav.timer = $interval(function() {
                    $scope.update(i)
                }, nav.intervall * 1000);
            }
        });



//      var response = [];
//      var key = $scope.bmf_current_dashboard.key;
//
//      response.push({
//          'class': 'sidebar-board',
//          'name': $scope.bmf_current_dashboard.name
//      });
//
//      $scope.bmf_sidebars[key].forEach(function(c, ci) {
//          response.push({'name': c.name});
//          c.views.forEach(function(v, vi) {
//              if ($scope.bmf_current_view && $scope.bmf_current_view.type == "list" && c.key == $scope.bmf_current_view.category.key && v.key == $scope.bmf_current_view.view.key) {
//                  response.push({'name': v.name, 'url': v.url, 'class': 'active'});
//              }
//              else {
//                  response.push({'name': v.name, 'url': v.url});
//              }
//          });
//      });
//
        console.log($scope.data);
    }
}]);
