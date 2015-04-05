import sublime_plugin, sublime
import re
import os.path
import json
from pprint import pprint

from time import time

class JITCoachEventCommand(sublime_plugin.EventListener):
  jitRegions = None

  def on_load(self, view):
    sublime.set_timeout(lambda:self.load(view, 'load'), 0)

  def on_post_save(self, view):
    sublime.set_timeout(lambda:self.save(view, 'post_save'), 0)

  def on_selection_modified(self, view):
    now = time()
    sublime.set_timeout(lambda:self.trigger(view, 'selection_modified'), 0)

  def find_region(self, jit, view):
    file_name = view.file_name();
    line = self.get_current_row_col(view)[0] + 1
    regions = jit["regions"]
    for i in range(0, len(regions)):
      if regions[i]["line"] == line:
        return  regions[i]
    return None
  
  def find_jit(self, view):
    file_name = view.file_name();
    jit_file_name = file_name + ".jit"
    if (os.path.exists(jit_file_name)):
      with open(jit_file_name) as data_file:    
        return json.load(data_file)
    return None

  def load(self, view, where):
    jit = self.find_jit(view)
    if jit:
      self.jitRegions = []
      for jitRegion in jit["regions"]:
        line = jitRegion["line"]
        point = view.text_point(line - 1, 0)
        region = view.line(sublime.Region(point, point));
        self.jitRegions.append(jitRegion)
        view.add_regions(str(line), [region], 'string', '', sublime.DRAW_NO_OUTLINE)

  def trigger(self, view, where):
    view_settings = view.settings()
    if view_settings.get('is_widget'):
      return

    if len(view.sel()) > 1:
      return
    else:
      view.hide_popup();
    
    jit = self.find_jit(view)
    if jit:
      region = None
      if self.jitRegions:
        for x in self.jitRegions:
          r = view.get_regions(str(x["line"]))
          if r and len(r) > 0:
            r = r[0]
            s = view.sel()[0]
            if s.a >= r.a and s.b <= r.b:
              region = x;
              break;

      if region:
        html = '<style>'
        html += '.success { color: darkgreen; font-weight: bold; }'
        html += '</style>'
        attempts = jit["opts"][region["index"]]["attempts"]
        for i in range(0, len(attempts)):
          attempt = attempts[i]
          if i == len(attempts) - 1:
            html += '<div class="success">'
          else:
            html += '<div>'
          html += attempt["strategy"] + ": " + attempt["outcome"] + "</div>"
        view.show_popup(html)

  def get_current_row_col(self, view):
    return view.rowcol(view.sel()[0].begin())
