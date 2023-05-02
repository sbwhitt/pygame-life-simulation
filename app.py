import pygame
import asyncio
import player
import entity
import colors
import map
import random
import settings

'''
x == width == rect.left
y == height == rect.top
'''

class App:
    def __init__(self):
        self._running = True
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.stats_width = settings.STATS_WIDTH
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width+self.stats_width, self.height), pygame.SCALED | pygame.RESIZABLE)
        # self.p = player.Player(int(self.width/2), 0)
        self.p = player.Player(1000, 1000)
        self.entities = []
        self.total_ent = 0
        self.keys = []
        self.dir_timer = 0
        self.move_timer = 0
        self.m = map.Map(self.width, self.height)
        self.avg_color = pygame.Color(0, 0, 0)
    
    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), settings.FONT_SIZE)
        self._build_entities()
        self.total_ent = len(self.entities)
        self._running = True
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self.keys.remove(event.unicode)
        if event.type == pygame.KEYDOWN:
            self._handlecmd(event.unicode, self.entities)
            self.keys.append(event.unicode)

    def on_loop(self):
        # if len(self.entities) == 0:
        #     self._running = False
        self.clock.tick(settings.CLOCK_RATE)
        # self.p.rect = self._handlekey(self.keys, self.p.rect)

        for e in self.entities:
            e.dir_timer += self.clock.get_time()
            e.move_timer += self.clock.get_time()
            self.m.grid[e.loc].remove(e)
            e.update(self.width, self.height)
            self.m.grid[e.loc].append(e)
    
    def on_render(self):
        self.screen.fill(colors.WHITE)
        # pygame.draw.rect(self.screen, colors.RED, self.p.rect)
        for e in self.entities:
            if self._p_collides(self.p, e) or e.age >= e.age_limit:
                self.m.grid[e.loc].remove(e)
                self.entities.remove(e)
                if settings.LOGGING: self._obituary(e)
            else:
                pygame.draw.rect(self.screen, e.color, e.rect)
                if len(self.m.grid[e.loc]) > 1:
                    if e.diseased:
                        self._spread_disease(self.m.grid[e.loc])
                    if random.randint(1, 3) == 1:
                        self._spread_color(self.m.grid[e.loc])
                if e.age_timer > settings.AGE_LENGTH:
                    e.age += 1
                    offspring = e.reproduce()
                    if offspring:
                        self.m.grid[offspring.loc].append(offspring)
                        self.entities.append(offspring)
                        self.total_ent += 1
                        self.avg_color = self._tally_avg_color(self._find_avg_color(self.entities))
                    e.age_timer = 0
                else:
                    e.age_timer += self.clock.get_time()
        self._display_stats()
        pygame.display.flip()

    def on_cleanup(self):
        print("total entities (at end): " + str(len(self.entities)))
        print("total entities (all time): " + str(self.total_ent))
        print("average color (last frame): " + str(self._find_avg_color(self.entities)))
        print("average color (all time): " + str(self.avg_color))
        pygame.quit()

    async def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            await asyncio.sleep(0)
        self.on_cleanup()
    
    # helpers
    def _add_start_entities(self):
        e0 = entity.Entity(0, 0, colors.RED)
        e1 = entity.Entity(self.width/2, 0, colors.GREEN)
        e2 = entity.Entity(self.width-settings.ENT_WIDTH, 0, colors.BLUE)
        e3 = entity.Entity(0, self.height-settings.ENT_WIDTH, colors.YELLOW)
        e4 = entity.Entity(self.width/2, self.height-settings.ENT_WIDTH, colors.CYAN)
        e5 = entity.Entity(self.width-settings.ENT_WIDTH, self.height-settings.ENT_WIDTH, colors.MAGENTA)
        for e in [e0, e1, e2, e3, e4, e5]:
            self.entities.append(e)
            self.m.grid[e.loc].append(e)

    def _build_entities(self):
        self._add_start_entities()
        self.avg_color = self._find_avg_color(self.entities)

    def _display_stats(self):
        ent_title = pygame.font.Font.render(self.font, "entities: ", True, colors.BLACK)
        ent_txt = pygame.font.Font.render(self.font, str(len(self.entities)), True, colors.BLACK)
        total_ent_title = pygame.font.Font.render(self.font, "entities all time: ", True, colors.BLACK)
        total_ent_txt = pygame.font.Font.render(self.font, str(self.total_ent), True, colors.BLACK)
        dis_ent_title = pygame.font.Font.render(self.font, "diseased entities: ", True, colors.BLACK)
        dis_ent_txt = pygame.font.Font.render(self.font, str(self._get_diseased_entities(self.entities)), True, colors.BLACK)
        avg_color_title = pygame.font.Font.render(self.font, "avg color", True, colors.BLACK)
        avg_color_txt = pygame.font.Font.render(self.font, str(self._find_avg_color(self.entities)), True, colors.BLACK)
        total_color_title = pygame.font.Font.render(self.font, "avg color all time", True, colors.BLACK)
        total_color_txt = pygame.font.Font.render(self.font, str(self.avg_color), True, colors.BLACK)
        self.screen.blit(ent_title, (self.width+10, 0))
        self.screen.blit(ent_txt, (self.width+10, settings.FONT_SIZE))
        self.screen.blit(total_ent_title, (self.width+10, settings.FONT_SIZE*2))
        self.screen.blit(total_ent_txt, (self.width+10, settings.FONT_SIZE*3))
        self.screen.blit(dis_ent_title, (self.width+10, settings.FONT_SIZE*4))
        self.screen.blit(dis_ent_txt, (self.width+10, settings.FONT_SIZE*5))
        self.screen.blit(avg_color_title, (self.width+10, settings.FONT_SIZE*6))
        self.screen.blit(avg_color_txt, (self.width+10, settings.FONT_SIZE*7))
        self.screen.blit(total_color_title, (self.width+10, settings.FONT_SIZE*8))
        self.screen.blit(total_color_txt, (self.width+10, settings.FONT_SIZE*9))
        pygame.draw.line(self.screen, colors.BLACK, (self.width, 0), (self.width, self.height))
    
    def _get_diseased_entities(self, entities):
        res = 0
        for e in entities:
            if e.diseased: res += 1
        return res

    def _p_collides(self, p, e):
        return p.loc == e.loc
    
    def _spread_color(self, collisions):
        r, g, b = 0, 0, 0
        highest_off = 0
        for e in collisions:
            highest_off = e.amnt_offspring if e.amnt_offspring > highest_off else highest_off
            r += e.color.r
            g += e.color.g
            b += e.color.b
        c = pygame.Color(int(r/len(collisions)), int(g/len(collisions)), int(b/len(collisions)))
        for e in collisions:
            e.color = c.lerp(e.color, 0.5)
    
    def _spread_disease(self, collisions):
        for e in collisions:
            if not e.diseased and random.randint(0, 1) == 1:
                e.diseased = True

    def _obituary(self, e):
        if e.diseased:
            print("an entity of generation " + str(e.generation) + " has perished from disease after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")
        else:
            print("an entity of generation " + str(e.generation) + " has perished after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")

    def _handlecmd(self, key, entities):
        if key == 'x':
            for i in range(int(len(entities)/2)):
                self._obituary(entities[i])
                self.m.grid[entities[i].loc].remove(entities[i])
                entities.pop(i)
        elif key == 'r':
            for e in entities:
                e.color = pygame.Color(random.randint(10, 245), random.randint(10, 245), random.randint(10, 245))
        elif key == '1':
            for e in entities:
                e.color.update(255, 0, 0)
        elif key == '2':
            for e in entities:
                e.color.update(0, 255, 0)
        elif key == '3':
            for e in entities:
                e.color.update(0, 0, 255)
        elif key == '4':
            for e in entities:
                e.color.update(255, 255, 0)
        elif key == '5':
            for e in entities:
                e.color.update(255, 0, 255)
        elif key == '6':
            for e in entities:
                e.color.update(0, 255, 255)
        elif key == 'c':
            for e in entities:
                r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
                e.color.update(g_cpy, b_cpy, r_cpy)
        elif key == 'f':
            for e in entities:
                r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
                e.color.update(255-g_cpy, 255-b_cpy, 255-r_cpy)
        elif key == 'e':
            self._add_start_entities()
        elif key == 'q':
            self._running = False

    def _handlekey(self, keys, rect):
        res = rect.copy()
        if 'w' in keys and rect.top != 0:
            res = res.move(0, -settings.ENT_WIDTH)
        if 'a' in keys and rect.left != 0:
            res = res.move(-settings.ENT_WIDTH, 0)
        if 's' in keys and rect.bottom != self.height:
            res = res.move(0, settings.ENT_WIDTH)
        if 'd' in keys and rect.right != self.width:
            res = res.move(settings.ENT_WIDTH, 0)
        self.p.loc = (res.left, res.top)
        return res

    def _find_avg_color(self, entities):
        r, g, b = 0, 0, 0
        for e in entities:
            r += e.color.r
            g += e.color.g
            b += e.color.b
        num_e = len(entities)
        return pygame.Color(int(r/num_e), int(g/num_e), int(b/num_e))
    
    # probably broken, is it obvious??
    def _tally_avg_color(self, current_avg):
        ents = len(self.entities)
        r, g, b = int(((ents-1)*self.avg_color.r + current_avg.r)/ents), int(((ents-1)*self.avg_color.g + current_avg.g)/ents), int(((ents-1)*self.avg_color.b + current_avg.b)/ents)
        return pygame.Color(r, g, b)
