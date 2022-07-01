import discord
from discord_components import Button

def limit(n,minN,maxN):
  return max(min(n,maxN),minN)

dispags = []

class DisPagClient:
  
  async def update(self,inter):
    for i in dispags:
      await i.button_clicked(inter)
  

class DisPag:
  def __init__(
    self,
    ctx,
    embeds : list,
    starting_index: int = 0,
    components: list = None
  ):
    self.ctx = ctx
    self.embeds = embeds
    for i in self.embeds:
      i.set_footer(text=f"сторінка {self.embeds.index(i)+1}/{len(self.embeds)}")
    self.idx = starting_index
    self.components = components
    self.forward = Button(emoji="➡️",custom_id="f")
    self.back = Button(emoji="⬅️", custom_id = 'b')
    self.message = None
    dispags.append(self)

  def get_components(self):
    returned = []
    try:
      for i in self.components:
        returned.append(i)
      returned.append([self.back,self.forward])
    except:
      returned.append([self.back,self.forward])
    return returned
    
  async def page_forward(self):
    self.idx+=1
    self.idx = limit(self.idx,0,len(self.embeds)-1)

    components = self.get_components()
    
    await self.message.edit(embed=self.embeds[self.idx], components = components)

  async def page_back(self):
    self.idx -= 1
    self.idx = limit(self.idx,0,len(self.embeds)-1)

    components = self.get_components()
    
    await self.message.edit(embed=self.embeds[self.idx], components = components)

  async def start(self):
    components = self.get_components()
    
    self.message = await self.ctx.send(embed=self.embeds[self.idx],components = components)

  async def button_clicked(self,inter):
    if(inter.custom_id == "f"):
      await self.page_forward()
    elif(inter.custom_id == "b"):
      await self.page_back()
