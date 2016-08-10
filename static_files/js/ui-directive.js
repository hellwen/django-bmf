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
            var url = LinkFactory("detail", scope.module, attr.bmfDetail, undefined);
            element.attr('href', url);

            element.on('click', function(event) {
                window.scrollTo(0,0);
            });
        }
    };
}]);

// manages links vom list views to detail views
bmfapp.directive('bmfDocumentUpload', ['ApiUrlFactory', function(ApiUrlFactory) {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attr) {
            var href = ApiUrlFactory(scope.parent_module, "documents", undefined, scope.pk);
            if (href) {
                element.attr('href', href + '#post-object-form');
                element.attr('target', '_blank');
            }
        }
    };
}]);


// manages form modal calls
bmfapp.directive('bmfForm', ['$rootScope', function($rootScope) {
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

                var url = attr.href;
                // new syntax - we must generate the link dynamically
                if (attr.href[0] == "#" && attr.bmfForm && attr.bmfPk) {
                    url = $rootScope.bmf_api.base + 'module/' + scope.module.ct + '/' + attr.bmfForm + '/' + attr.bmfPk + '/' + attr.href.substr(1);
                }

                var dict = $.bmf.AJAX;
                dict.type = "GET";
                dict.url = url;
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

                    var url = ApiUrlFactory(view.module, 'detail', null, view.kwargs.pk);
                    $http.get(url).then(function(response) {
                        scope.ui.workflow = response.data.workflow;
                        scope.ui.reports = [];
                        for (var key in response.data.reports) {
                            var report = response.data.reports[key];
                            console.log("REPORT", report)
                            var url = ApiUrlFactory(view.module, 'report', report.slug, view.kwargs.pk);
                            scope.ui.reports[key] = {
                                verbose_name: report.verbose_name,
                                name: report.name,
                                has_form: report.has_form,
                                url: url
                            }
                        }
                        scope.ui.views = response.data.views;
                        scope.ui.notifications = response.data.notifications;
                        scope.template_html = response.data.html
                        $rootScope.bmfevent_objectdata(response.data.object);
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
            $scope.hidden_selector = undefined;
            $scope.parent_module = null;
            $scope.parent_object = null;
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
                if (search.open) {
                    $scope.hidden_selector = search.hidden;
                }
                else {
                    $scope.hidden_selector = undefined;
                }

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

            $scope.$on(BMFEVENT_OBJECTDATA, function(event, data) {
                $scope.parent_object = data;
            });

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
