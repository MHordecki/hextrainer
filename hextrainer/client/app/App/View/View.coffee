
root: App.View: {}

root.views = {}

root.views.welcome: ->
  "<p>Witaj w Hex Trainerze!</p><p><a href=\"javascript:App.currentApp.switchPage('training')\"><b>Rozpocznij trening</b></a>.</p>"

root.views.loading: ->
  "<div style=\"width:100%;height100px;text-align:center;\">
  <img src=\"/media/ajax-loader.gif\" /><br/>Ładowanie</div>"

class root.View
  constructor: (app) ->
    @app: app

  update_content: (page, data) ->
    $('#content').html(root.views[page](data))

