
App: window.App: {}

App.init:  ->
    App.currentApp: new App.App()
    App.currentApp.init()

class App.App
    constructor: ->
        @currentPage: undefined
        @view: undefined

    switchPage: (name, ok, bad) ->
        exit_ok: =>
            @currentPage: new App.Pages.pages[name] @, @view
            @currentPage.enter()
            ok() if ok
        exit_bad: =>
            bad() if bad
          
        if App.Pages.pages[name]?
            if @currentPage
                @currentPage.exit exit_ok, exit_bad
            else
                exit_ok()
        else
            console.log "Error!! Page $name does not exist"

    init: ->
        @view: new App.View.View @

class App.Error
    constructor: (msg) ->
        @msg: msg

