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
                scope.activity = undefined;

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
                        console.log(response);

                        if (response.data.views.activity.enabled) {
                            var url = view.module.base + view.pk  + '/';
                            $http.get(url).then(function(response) {
                                console.log(response);
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
