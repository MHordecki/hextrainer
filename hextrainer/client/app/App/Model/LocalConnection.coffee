
class App.Model.NonLocalQueryError extends App.Error

## App.Model.LocalConnection
## =========================
## Uses localStorage as its sole source.
class App.Model.LocalConnection
    constructor: (handler) ->
        @handler: handler

    isOnline: ->
        false
