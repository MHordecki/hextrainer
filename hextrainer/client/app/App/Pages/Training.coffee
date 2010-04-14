
root: App.Pages

class root.Training
  constructor: (app, view) ->
    @app: app
    @view: view

  enter: ->
    @view.update_content 'loading'
  
  exit: (ok, bad) ->
    ok()

root.pages['training']: root.Training

