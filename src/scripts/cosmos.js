(function () {
  'use strict';

  var STORAGE_KEY = 'cosmos';
  var EVENT_NAME = 'cosmos-update';

  var COSMOS_CONFIG = [
    {"key": "ip",     "label": "Target IP",       "default": "10.10.10.10", "type": "string",  "placeholder": "10.10.10.10"},
    {"key": "port",   "label": "Target Port",     "default": "9001",       "type": "number",  "placeholder": "9001"},
    {"key": "lhost",  "label": "Listener IP",     "default": "10.0.0.1",   "type": "string",  "placeholder": "10.0.0.1"},
    {"key": "lport",  "label": "Listener Port",   "default": "443",        "type": "number",  "placeholder": "443"},
    {"key": "domain", "label": "Target Domain",   "default": "example.local", "type": "string", "placeholder": "example.local"},
    {"key": "user",   "label": "Username",        "default": "admin",      "type": "string",  "placeholder": "admin"},
    {"key": "shell",  "label": "Shell Path",      "default": "/bin/sh",    "type": "string",  "placeholder": "/bin/sh"}
  ];

  var CONFIG_MAP = {};
  COSMOS_CONFIG.forEach(function (c) { CONFIG_MAP[c.key] = c; });

  var state = {};
  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) { state = JSON.parse(raw) || {}; }
    } catch (_) { state = {}; }
    COSMOS_CONFIG.forEach(function (c) {
      if (state[c.key] === undefined || state[c.key] === null) {
        state[c.key] = c.default;
      }
    });
  }
  loadState();

  function persistState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
  }

  function notify(key, value) {
    var evt = new CustomEvent(EVENT_NAME, {
      detail: { key: key, value: value, state: getSnapshot() },
      bubbles: true
    });
    document.dispatchEvent(evt);
  }

  function getSnapshot() {
    var s = {};
    COSMOS_CONFIG.forEach(function (c) { s[c.key] = state[c.key]; });
    return s;
  }

  window.Cosmos = {
    get: function (key) { return state[key]; },
    set: function (key, value) {
      if (CONFIG_MAP[key]) {
        var type = CONFIG_MAP[key].type;
        if (type === 'number') { value = Number(value); }
        state[key] = value;
        persistState();
        notify(key, value);
      }
    },
    getAll: function () { return getSnapshot(); },
    reset: function () {
      COSMOS_CONFIG.forEach(function (c) { state[c.key] = c.default; });
      persistState();
      notify('*', null);
    },
    onChange: function (fn) {
      document.addEventListener(EVENT_NAME, function (e) { fn(e.detail); });
    },
    getConfig: function () { return COSMOS_CONFIG; }
  };
})();
