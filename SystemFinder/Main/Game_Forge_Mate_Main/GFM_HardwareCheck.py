import requests


class GameHardwareChecker:
    def __init__(self):
        self.games_api_url = "http://127.0.0.1:5000/games"
        self.cpu_api_url = "http://127.0.0.1:5000/cpu"
        self.gpu_api_url = "http://127.0.0.1:5000/gpu"
        self.games_data = self.fetch_data(self.games_api_url)
        self.cpu_data = self.fetch_data(self.cpu_api_url)
        self.gpu_data = self.fetch_data(self.gpu_api_url)

    def fetch_data(self, api_url):
        response = requests.get(api_url)
        return response.json()

    def find_highest_ranked_hardware(self, searched_games):
        highest_cpu_rank = float('inf')
        highest_gpu_rank = float('inf')
        highest_cpu = None
        highest_gpu = None

        for searched_game in searched_games:
            found_game = next((game for game in self.games_data if searched_game.lower() in game["name"].lower()), None)

            if found_game:
                print("Oyun Bulundu:", found_game["name"])

                if "CPU:" in found_game:
                    highest_cpu, highest_cpu_rank = self.check_cpu_requirement(found_game, highest_cpu, highest_cpu_rank)

                if "Graphics Card:" in found_game:
                    highest_gpu, highest_gpu_rank = self.check_gpu_requirement(found_game, highest_gpu, highest_gpu_rank)

        return highest_cpu, highest_cpu_rank, highest_gpu, highest_gpu_rank

    def check_cpu_requirement(self, game, highest_cpu, highest_cpu_rank):
        cpu_requirement = game["CPU:"].split(" or ")[0].strip().lower()
        found_cpu = next((cpu for cpu in self.cpu_data if cpu_requirement in cpu["Model"].lower()), None)
        if found_cpu and int(found_cpu["Rank"]) < highest_cpu_rank:
            highest_cpu_rank = int(found_cpu["Rank"])
            highest_cpu = found_cpu

        print("Gerekli CPU:", game["CPU:"])


        return highest_cpu, highest_cpu_rank

    def check_gpu_requirement(self, game, highest_gpu, highest_gpu_rank):
        gpu_requirement_part = game["Graphics Card:"].split(" or ")[0].split(" ")[-2:]
        gpu_requirement_part = " ".join(gpu_requirement_part).lower()
        found_gpus = [gpu for gpu in self.gpu_data if gpu_requirement_part in gpu["Model"].lower()]
        if found_gpus:
            highest_rank_gpu = min(found_gpus, key=lambda gpu: int(gpu["Rank"]))
            if int(highest_rank_gpu["Rank"]) < highest_gpu_rank:
                highest_gpu_rank = int(highest_rank_gpu["Rank"])
                highest_gpu = highest_rank_gpu
        print("Gerekli GPU:", game["Graphics Card:"])
        return highest_gpu, highest_gpu_rank
