(function(){
  var App;
  App = (window.App = {});
  App.init = function init() {
    App.currentApp = new App.App();
    return App.currentApp.init();
  };
  App.App = function App() {
    this.currentPage = undefined;
    this.view = undefined;
    return this;
  };
  App.App.prototype.switchPage = function switchPage(name, ok, bad) {
    var _a, exit_bad, exit_ok;
    exit_ok = (function(__this) {
      var __func = function() {
        this.currentPage = new App.Pages.pages[name](this, this.view);
        this.currentPage.enter();
        if (ok) {
          return ok();
        }
      };
      return (function exit_ok() {
        return __func.apply(__this, arguments);
      });
    })(this);
    exit_bad = (function(__this) {
      var __func = function() {
        if (bad) {
          return bad();
        }
      };
      return (function exit_bad() {
        return __func.apply(__this, arguments);
      });
    })(this);
    if ((typeof (_a = App.Pages.pages[name]) !== "undefined" && _a !== null)) {
      if (this.currentPage) {
        return this.currentPage.exit(exit_ok, exit_bad);
      } else {
        return exit_ok();
      }
    } else {
      return console.log("Error!! Page " + name + " does not exist");
    }
  };
  App.App.prototype.init = function init() {
    this.view = new App.View.View(this);
    return this.view;
  };
  App.Error = function Error(msg) {
    this.msg = msg;
    return this;
  };
})();

(function(){
  var root;
  root = (App.Pages = {});
  root.pages = {};
})();

(function(){
  var root;
  root = App.Pages;
  root.Welcome = function Welcome(app, view) {
    this.app = app;
    this.view = view;
    return this;
  };
  root.Welcome.prototype.enter = function enter() {
    return this.view.update_content('welcome');
  };
  root.Welcome.prototype.exit = function exit(ok, bad) {
    return ok();
  };
  root.pages['welcome'] = root.Welcome;
})();

(function(){
  var root;
  root = App.Pages;
  root.Training = function Training(app, view) {
    this.app = app;
    this.view = view;
    return this;
  };
  root.Training.prototype.enter = function enter() {
    return this.view.update_content('loading');
  };
  root.Training.prototype.exit = function exit(ok, bad) {
    return ok();
  };
  root.pages['training'] = root.Training;
})();

(function(){
  var root;
  root = (App.View = {});
  root.views = {};
  root.views.welcome = function welcome() {
    return "<p>Witaj w Hex Trainerze!</p><p><a href=\"javascript:App.currentApp.switchPage('training')\"><b>Rozpocznij trening</b></a>.</p>";
  };
  root.views.loading = function loading() {
    return "<div style=\"width:100%;height100px;text-align:center;\"> \
<img src=\"/media/ajax-loader.gif\" /><br/>Ładowanie</div>";
  };
  root.View = function View(app) {
    this.app = app;
    return this;
  };
  root.View.prototype.update_content = function update_content(page, data) {
    return $('#content').html(root.views[page](data));
  };
})();

(function(){
  App.init();
  App.currentApp.switchPage('welcome');
})();
