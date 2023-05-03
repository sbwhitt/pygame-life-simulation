import pygame
import asyncio
import entity
import colors
import map
import stats
import random
import settings

'''
x == width == rect.left
y == height == rect.top
'''

class App:
    def __init__(self):
        self._running = True
        self.paused = False
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width + settings.STATS_WIDTH, self.height), pygame.SCALED | pygame.RESIZABLE)
        self.entities = []
        self.total_ent = 0
        self.keys = []
        self.dir_timer = 0
        self.move_timer = 0
        self.m = map.Map(self.width, self.height)
        self.stats = stats.Stats(self.screen, self.width)
        self.avg_color = pygame.Color(0, 0, 0)
    
    def on_init(self):
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
        if self.paused:
            return
        self.clock.tick(settings.CLOCK_RATE)
        for e in self.entities:
            e.dir_timer += self.clock.get_time()
            e.move_timer += self.clock.get_time()
            self.m.grid[e.loc].remove(e)
            e.update(self.width, self.height)
            self.m.grid[e.loc].append(e)
    
    def on_render(self):
        self.screen.fill(colors.WHITE)
        for e in self.entities:
            if self.paused:
                pygame.draw.rect(self.screen, e.color, e.rect)
                continue
            if e.age >= e.age_limit:
                self.m.grid[e.loc].remove(e)
                self.entities.remove(e)
                self._obituary(e)
                continue
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

        self._update_stats()
        pygame.display.flip()

    def on_cleanup(self):
        if settings.LOGGING:
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
        for e in [
            entity.Entity(0, 0, colors.RED),
            entity.Entity(self.width/2, 0, colors.GREEN),
            entity.Entity(self.width-settings.ENT_WIDTH, 0, colors.BLUE),
            entity.Entity(0, self.height-settings.ENT_WIDTH, colors.YELLOW),
            entity.Entity(self.width/2, self.height-settings.ENT_WIDTH, colors.CYAN),
            entity.Entity(self.width-settings.ENT_WIDTH, self.height-settings.ENT_WIDTH, colors.MAGENTA)
        ]:
            self.entities.append(e)
            self.m.grid[e.loc].append(e)

    def _build_entities(self):
        self._add_start_entities()
        self.avg_color = self._find_avg_color(self.entities)

    def _update_stats(self):
        self.stats.clear()
        self.stats.add_line("entities: ")
        self.stats.add_line(str(len(self.entities)))
        self.stats.add_line("entities all time: ")
        self.stats.add_line(str(self.total_ent))
        self.stats.add_line("diseased entities: ")
        self.stats.add_line(str(self._get_diseased_entities(self.entities)))
        self.stats.add_line("avg color")
        avg_color = self._find_avg_color(self.entities)
        self.stats.add_line(str(avg_color), avg_color)
        self.stats.add_line("avg color all time")
        self.stats.add_line(str(self.avg_color), self.avg_color)
        self.stats.draw_lines()
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
        if not settings.LOGGING:
            return
        if e.diseased:
            print("an entity of generation " + str(e.generation) + " has perished from disease after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")
        else:
            print("an entity of generation " + str(e.generation) + " has perished after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")

    def _handlecmd(self, key, entities):
        if key == 'x' and not self.paused:
            for i in range(int(len(entities)/2)):
                self._obituary(entities[i])
                self.m.grid[entities[i].loc].remove(entities[i])
                entities.pop(i)
        elif key == 'r' and not self.paused:
            for e in entities:
                e.color = pygame.Color(random.randint(10, 245), random.randint(10, 245), random.randint(10, 245))
        elif key == '1' and not self.paused:
            for e in entities:
                e.color.update(255, 0, 0)
        elif key == '2' and not self.paused:
            for e in entities:
                e.color.update(0, 255, 0)
        elif key == '3' and not self.paused:
            for e in entities:
                e.color.update(0, 0, 255)
        elif key == '4' and not self.paused:
            for e in entities:
                e.color.update(255, 255, 0)
        elif key == '5' and not self.paused:
            for e in entities:
                e.color.update(255, 0, 255)
        elif key == '6' and not self.paused:
            for e in entities:
                e.color.update(0, 255, 255)
        elif key == 'c' and not self.paused:
            for e in entities:
                r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
                e.color.update(g_cpy, b_cpy, r_cpy)
        elif key == 'f' and not self.paused:
            for e in entities:
                r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
                e.color.update(255-g_cpy, 255-b_cpy, 255-r_cpy)
        elif key == 'e' and not self.paused:
            self._add_start_entities()
        elif key == 'q':
            self._running = False
        # escape key
        elif key == '\x1b':
            self.paused = not self.paused

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
