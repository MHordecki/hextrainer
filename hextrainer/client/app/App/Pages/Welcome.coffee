
root: App.Pages

class root.Welcome
  constructor: (app, view) ->
    @app: app
    @view: view

  enter: ->
    @view.update_content 'welcome'
  
  exit: (ok, bad) ->
    ok()

root.pages['welcome']: root.Welcome

