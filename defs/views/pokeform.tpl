<form id="poke_sug" action="{{action}}" method="get">
% member_num = len(members)
% for x in range(6):
  <input class="pokecomplete" type="input" name="poke{{x}}" value="{{members[x].name if x < member_num else ""}}"><br>
% end 
  <input type="submit" value="送信">
