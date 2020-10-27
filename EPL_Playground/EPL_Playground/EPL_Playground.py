
from fpl import FPL
import aiohttp
import asyncio
from idandpwd import getPWD
from idandpwd import getID
import plotly.graph_objects as go

async def main():
      
      async with aiohttp.ClientSession() as session:
          linefig = go.Figure()
          fpl = FPL(session)
          await fpl.login(getID(),getPWD())
          classic_league = await fpl.get_classic_league(237300)
          standings = await classic_league.get_standings(1,1,1)
          print(standings['results'])
          listofids=[]
          for user in standings['results']:
              listofids.append(user['entry'])

          idtolostpoints = dict()
          for id in listofids:
           user = await fpl.get_user(id)
           print(str(user))
           history = await user.get_gameweek_history()
           points=[]
           gw=[]
           lostpoints = 0;
           for gwhistory in history:
            points.append(gwhistory['total_points'])
            gw.append(gwhistory['event'])
            lostpoints=lostpoints + gwhistory['points_on_bench']
           
           linefig.add_trace(go.Scatter(x=gw, y=points, name=str(user),  mode='lines',
                         line=dict(width=2)))
           idtolostpoints[str(user)]=lostpoints
          
          for key in idtolostpoints:
           print(key + ":" + str(idtolostpoints[key]))
          linefig.update_layout(title_text="Melawatians Total Points Every Game Week")
          linefig.show()
  
asyncio.run(main())