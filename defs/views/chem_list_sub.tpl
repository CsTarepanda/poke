% atk, dfc = party.ad_list()
% atk_chem = sorted(atk.items(), key=lambda x: x[0].id)
% dfc_chem = sorted(dfc.items(), key=lambda x: x[0].id)

<tr>
  <th class="atk">atk</th>
  % for t in atk_chem:
    <th style="background: rgb(255, {{",".join([str(int(100 + 50 * t[1])) for x in range(2)])}})">{{t[1]}}</th>
  % end
</tr>
<tr>
  <th class="dfc">dfc</th>
  % for t in dfc_chem:
    <th style="background: rgb({{",".join([str(int(200 - 50 * t[1])) for x in range(2)])}}, 255)">{{t[1]}}</th>
  % end
</tr>
