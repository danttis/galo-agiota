import json
import random
import os
from datetime import datetime

# Bounds para genes de capanga
BOUNDS_CAPANGA = {
    "raio_visao": (200.0, 500.0),
    "raio_ataque": (150.0, 400.0),
    "vel_perseguir": (1.0, 3.5),
    "vel_patru": (0.5, 2.5),
    "tempo_tiro_min": (20, 100),
    "tempo_tiro_max": (50, 180),
    "preferencia_dist": (50.0, 300.0),
    "prob_pular": (0.0, 0.8),
    "prob_recuar": (0.0, 0.8),
    "anticipacao_y": (-30.0, 30.0),
    "coordenacao": (0.0, 1.0),
    "precisao_aim": (0.0, 1.0),
}

# Bounds para genes de boss
BOUNDS_BOSS = {
    "prob_perseguir": (0.1, 0.5),
    "prob_atirar": (0.2, 0.5),
    "prob_pular": (0.1, 0.4),
    "prob_invocar": (0.05, 0.3),
    "vel_perseguir": (2.0, 5.0),
    "tempo_tiro_base": (15, 50),
    "disparos_por_salva": (1, 5),
    "anticipacao_y": (-20.0, 20.0),
    "distancia_otima": (50.0, 300.0),
    "precisao_aim": (0.3, 1.0),
}

DEFAULT_GENES = {
    "capanga": {
        "raio_visao": 300.0,
        "raio_ataque": 250.0,
        "vel_perseguir": 1.5,
        "vel_patru": 1.5,
        "tempo_tiro_min": 60,
        "tempo_tiro_max": 120,
        "preferencia_dist": 50.0,
        "prob_pular": 0.0,
        "prob_recuar": 0.0,
        "anticipacao_y": 0.0,
        "coordenacao": 0.0,
        "precisao_aim": 0.0,
    },
    "boss": {
        "prob_perseguir": 0.25,
        "prob_atirar": 0.35,
        "prob_pular": 0.2,
        "prob_invocar": 0.2,
        "vel_perseguir": 3.0,
        "tempo_tiro_base": 40,
        "disparos_por_salva": 3,
        "anticipacao_y": 0.0,
        "distancia_otima": 150.0,
        "precisao_aim": 0.5,
    },
}


def _clamp(val, low, high):
    return max(low, min(high, val))


def _random_gene(bounds):
    gene = {}
    for key, (low, high) in bounds.items():
        if isinstance(low, int):
            gene[key] = random.randint(low, high)
        else:
            gene[key] = random.uniform(low, high)
    return gene


def _mutate_gene(gene, bounds, sigma=0.1):
    mutated = dict(gene)
    for key, (low, high) in bounds.items():
        span = high - low
        noise = random.gauss(0, span * sigma)
        mutated[key] = _clamp(gene[key] + noise, low, high)
        if isinstance(low, int):
            mutated[key] = int(round(mutated[key]))
    return mutated


def _crossover(g1, g2, bounds):
    child = {}
    for key, (low, high) in bounds.items():
        alpha = random.random()
        child[key] = _clamp(alpha * g1[key] + (1 - alpha) * g2[key], low, high)
        if isinstance(low, int):
            child[key] = int(round(child[key]))
    return child


class PlayerProfiler:
    def __init__(self):
        self.shots_fired = 0
        self.shots_hit = 0
        self.jumps_total = 0
        self.frames_enemy_near = 0
        self.frames_in_air = 0
        self.bribes_thrown = 0
        self.bribes_successful = 0
        self.player_deaths = 0
        self.sum_distances = 0.0
        self.distance_samples = 0
        self.last_profile_frame = 0

    def profile(self, jogador, inimigos, tiros_jogador, frame_count):
        self.last_profile_frame = frame_count

        if not getattr(jogador, 'no_chao', True):
            self.frames_in_air += 1

        # Distancia media ate inimigos vivos e nao subornados
        dists = []
        for ini in inimigos:
            if not ini.alive() or ini.morto or getattr(ini, 'subornado', False):
                continue
            dx = ini.rect.centerx - jogador.rect.centerx
            dy = ini.rect.centery - jogador.rect.centery
            dists.append((dx * dx + dy * dy) ** 0.5)
        if dists:
            d = sum(dists) / len(dists)
            self.sum_distances += d
            self.distance_samples += 1
            if d < 250:
                self.frames_enemy_near += 1

    def to_dict(self):
        return {
            "shots_fired": self.shots_fired,
            "shots_hit": self.shots_hit,
            "jumps_total": self.jumps_total,
            "frames_enemy_near": self.frames_enemy_near,
            "frames_in_air": self.frames_in_air,
            "bribes_thrown": self.bribes_thrown,
            "bribes_successful": self.bribes_successful,
            "player_deaths": self.player_deaths,
            "sum_distances": self.sum_distances,
            "distance_samples": self.distance_samples,
        }

    def from_dict(self, d):
        for k in self.to_dict().keys():
            setattr(self, k, d.get(k, 0))


class GenePool:
    TAMANHO = 12
    MORTES_POR_EVOLUCAO = 3
    SIGMA = 0.1
    FRESH_BLOOD = 0.1

    def __init__(self, tipo, bounds, default):
        self.tipo = tipo
        self.bounds = bounds
        self.default = default
        self.generation = 1
        self.genes = []
        self.mortes_desde_evolucao = 0
        self._init_population()

    def _init_population(self):
        for _ in range(self.TAMANHO):
            g = dict(self.default)
            g["generation"] = 1
            self.genes.append({"gene": g, "fitness": 0.0, "generation": 1})

    def get_brain(self):
        # Seleciona com probabilidade proporcional ao fitness (se houver fitness > 0)
        total = sum(max(0.1, g["fitness"] + 1.0) for g in self.genes)
        r = random.uniform(0, total)
        acc = 0.0
        for g in self.genes:
            acc += max(0.1, g["fitness"] + 1.0)
            if r <= acc:
                return dict(g["gene"])
        return dict(self.genes[-1]["gene"])

    def report_death(self, enemy_stats):
        fitness = self._calc_fitness(enemy_stats)
        # Substitui o pior gene
        worst = min(self.genes, key=lambda g: g["fitness"])
        worst["gene"] = dict(enemy_stats.get("brain", self.default))
        worst["fitness"] = fitness
        worst["generation"] = self.generation
        self.mortes_desde_evolucao += 1
        if self.mortes_desde_evolucao >= self.MORTES_POR_EVOLUCAO:
            self.mortes_desde_evolucao = 0
            self._evoluir()

    def _calc_fitness(self, stats):
        survival = stats.get("survival_frames", 0) / 60.0
        damage = stats.get("damage_dealt", 0)
        dist_sum = stats.get("sum_dist", 0.0)
        dist_samples = stats.get("dist_samples", 1)
        dist_avg = dist_sum / max(1, dist_samples)
        fit = survival * 10.0 + damage * 25.0
        if 100 < dist_avg < 300:
            fit += 20.0
        return fit

    def _evoluir(self):
        # Ordena por fitness
        self.genes.sort(key=lambda g: g["fitness"], reverse=True)
        melhor = self.genes[0]
        # Substituir 4 piores
        for i in range(self.TAMANHO - 4, self.TAMANHO):
            if random.random() < self.FRESH_BLOOD:
                self.genes[i]["gene"] = _random_gene(self.bounds)
            elif i == self.TAMANHO - 1:
                # Elite
                self.genes[i]["gene"] = dict(melhor["gene"])
            elif i == self.TAMANHO - 2:
                # Crossover
                p1 = self._torneio()
                p2 = self._torneio()
                self.genes[i]["gene"] = _crossover(p1["gene"], p2["gene"], self.bounds)
            else:
                # Mutacao
                pai = self._torneio()
                self.genes[i]["gene"] = _mutate_gene(pai["gene"], self.bounds, self.SIGMA)
            self.genes[i]["fitness"] = 0.0
            self.genes[i]["generation"] = self.generation + 1
        self.generation += 1

    def _torneio(self, k=3):
        amostra = random.sample(self.genes, min(k, len(self.genes)))
        return max(amostra, key=lambda g: g["fitness"])

    def to_dict(self):
        return {
            "generation": self.generation,
            "genes": self.genes,
        }

    def from_dict(self, d):
        self.generation = d.get("generation", 1)
        self.genes = d.get("genes", [])
        if len(self.genes) < self.TAMANHO:
            self._init_population()


class AdaptationEngine:
    ARQUIVO = "data/ia_memoria.json"

    def __init__(self):
        self.profiler = PlayerProfiler()
        self.pools = {
            "capanga": GenePool("capanga", BOUNDS_CAPANGA, DEFAULT_GENES["capanga"]),
            "boss": GenePool("boss", BOUNDS_BOSS, DEFAULT_GENES["boss"]),
        }
        self.session_count = 0
        self.history = []
        self._load()
        self.session_count += 1

    def get_brain(self, tipo):
        if tipo in self.pools:
            return self.pools[tipo].get_brain()
        return dict(DEFAULT_GENES.get(tipo, {}))

    def report_death(self, enemy):
        stats = getattr(enemy, '_adaptive_stats', {})
        brain = getattr(enemy, 'brain', None)
        if brain:
            stats["brain"] = brain
        # Determina tipo
        from entidades.boss import Boss, BossVisitante
        if isinstance(enemy, (Boss, BossVisitante)):
            self.pools["boss"].report_death(stats)
        else:
            self.pools["capanga"].report_death(stats)

    def profile_player(self, jogador, inimigos, tiros_jogador, frame_count):
        self.profiler.profile(jogador, inimigos, tiros_jogador, frame_count)

    def save(self):
        data = {
            "version": 1,
            "session_count": self.session_count,
            "timestamp": datetime.now().isoformat(),
            "player_profile": self.profiler.to_dict(),
            "pools": {k: v.to_dict() for k, v in self.pools.items()},
            "history": self.history,
        }
        os.makedirs(os.path.dirname(self.ARQUIVO), exist_ok=True)
        with open(self.ARQUIVO, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        if not os.path.exists(self.ARQUIVO):
            return
        try:
            with open(self.ARQUIVO, "r") as f:
                data = json.load(f)
            self.session_count = data.get("session_count", 0)
            self.profiler.from_dict(data.get("player_profile", {}))
            for k, v in data.get("pools", {}).items():
                if k in self.pools:
                    self.pools[k].from_dict(v)
            self.history = data.get("history", [])
        except Exception:
            pass

    def get_adaptation_level(self):
        """Retorna percentual medio de evolucao das pools."""
        total_gen = sum(p.generation for p in self.pools.values())
        max_gen = len(self.pools) * 50
        return min(100, int((total_gen / max_gen) * 100))
