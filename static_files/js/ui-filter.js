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

// http://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
app.filter('timesince', ['$filter', function($filter) {
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
