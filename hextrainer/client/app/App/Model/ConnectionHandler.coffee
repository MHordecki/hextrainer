
class App.Model.ConnectionHandler
    constructor: ->
        @current: new App.Model.LocalConnection @
    
    isOnline: ->
        @current.isOnline()

    getCurrentConnection: ->
        @current

    goOnline: (callback) ->
        false
