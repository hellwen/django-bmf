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
