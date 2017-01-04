% rebase("base.tpl", title="")
% members = party.members

% atk, dfc = party.ad_list()
% atk = len([x for x in atk.values() if x > 1])
% dfc = len([x for x in dfc.values() if x < 1])
<h1>全パターン解析<small>atk: {{atk}} dfc: {{dfc}} atk+dfc: {{atk + dfc}}</small></h1>

<div style="float: left; margin-right: 20px">
  % include("pokeform.tpl", action="/all")
  </form>
</div>

% include("chem_list.tpl")

<div style="float: left">
  <p>atk max: {{max_list[0]}} dfc max: {{max_list[1]}} atk+dfc max: {{max_list[2]}}</p>
  <table class="table table-bordered table-hover">
    <thead>
      <tr id="head" align="left">
        <th id="atk_sort"><span class="btn atk">atk</span></th>
        <th id="dfc_sort"><span class="btn dfc">dfc</span></th>
        <th id="atk_dfc_sort"><span class="btn atk_dfc">atk+dfc</span></th>
        <th>タイプ</th>
        <th>ポケモン</th>
      </tr>
    </thead>
    <tbody id="suggest_list">
    </tbody>
  </table>
</div>

<style>
.atk{
  background: rgb(255, 200, 200);
}

.dfc{
  background: rgb(200, 200, 255);
}

.atk_dfc{
  background: rgb(255, 200, 255);
}
</style>

<script>
function view(chemistries){
  let $suggest_list = $("#suggest_list");
  $suggest_list.empty()
  $.each(chemistries, function(i, chem){
    let tr = $("<tr>");
    tr.append($("<td>", {text: chem[0]}));
    tr.append($("<td>", {text: chem[1]}));
    tr.append($("<td>", {text: chem[0] + chem[1]}));
    tr.append($("<td>", {text: chem[2]}));
    tr.append($("<td>", {text: chem[3]}));
    $suggest_list.append(tr);
  });
}

let chemistries = {{!chemistries}};

function atk_sort(chemistries){
  chemistries.sort(function(a, b){
    if(a[0] < b[0]) return 1;
    if(a[0] > b[0]) return -1;
    return 0;
  });
  return chemistries;
}

function dfc_sort(chemistries){
  chemistries.sort(function(a, b){
    if(a[1] < b[1]) return 1;
    if(a[1] > b[1]) return -1;
    return 0;
  });
  return chemistries;
}

function atk_dfc_sort(chemistries){
  chemistries.sort(function(a, b){
    if(a[0] + a[1] < b[0] + b[1]) return 1;
    if(a[0] + a[1] > b[0] + b[1]) return -1;
    return 0;
  });
  return chemistries;
}

$(function(){
  view(dfc_sort(chemistries));

  $("#atk_sort").on("click", function(){
    view(atk_sort(chemistries));
  });

  $("#dfc_sort").on("click", function(){
    view(dfc_sort(chemistries));
  });

  $("#atk_dfc_sort").on("click", function(){
    view(atk_dfc_sort(chemistries));
  });
});
</script>
% include("pokecomplete.tpl")
