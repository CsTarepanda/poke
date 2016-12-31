% from calc_chemistry import Party
% from bottle import template
    
<table id="chem_list" class="table table-bordered table-hover" style="width: 70%">
  <thead>
    <tr>
      % head = 8
      <th width="{{head}}%" id="chem_list_name">all</th>
      %types = [ "ノ", "炎", "水", "電", "草", "氷", "格", "毒", "地", "飛", "超", "虫", "岩", "霊", "竜", "悪", "鋼", "妖"]
      % for t in types:
        <th width="{{(100 - head) / len(types)}}%">{{t}}</th>
      % end
    </tr>
  </thead>

  <tbody id="chem_list_all">
    % include("chem_list_sub.tpl", party=party)
  </tbody>
  % for index, member in enumerate(party.members):
    <tbody id="chem_list_{{index}}" style="display: none">
      % include("chem_list_sub.tpl", party=Party(member.name))
    </tbody>
  % end
</table>

<div id="member_choice">
  % for index, member in enumerate(party.members):
    <span id="member_choice{{index}}">{{member.name}}</span>
  % end
</div>

<script>
  % for index, member in enumerate(members):
    $("#member_choice #member_choice{{index}}").on({
      "mouseenter": function(){
        $("#chem_list #chem_list_all").hide();
        $("#chem_list #chem_list_{{index}}").show();
        $("#chem_list_name").text("{{member.name[:1]}}");
      },
      "mouseleave": function(){
        $("#chem_list #chem_list_{{index}}").hide();
        $("#chem_list #chem_list_all").show();
        $("#chem_list_name").text("all");
      }
    });
  % end
</script>
