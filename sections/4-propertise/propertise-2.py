class Tablet:
    SUPPORTED_MODELS = {
        "lite": {"base_storage": 32, "memory": 2},
        "pro": {"base_storage": 64, "memory": 3},
        "max": {"base_storage": 128, "memory": 4},
    }

    MAX_STORAGE = 1024

    def __init__(self, model):
        self._model = model
        self._base_storage = Tablet.SUPPORTED_MODELS[model]["base_storage"]
        self._memory = Tablet.SUPPORTED_MODELS[model]["memory"]
        self._added_storage = 0

    def __repr__(self):
        return f"Tablet(model='{self._model}', base_storage={self.base_storage}, added_storage={self._added_storage}, memory={self.memory})"

    @property
    def model(self):
        return self._model

    @property
    def storage(self):
        return self.base_storage + self._added_storage

    @property
    def memory(self):
        return Tablet.SUPPORTED_MODELS[self._model]["memory"]

    @property
    def base_storage(self):
        return Tablet.SUPPORTED_MODELS[self._model]["base_storage"]

    def add_storage(self, extra_storage):
        if extra_storage > Tablet.MAX_STORAGE:
            raise ValueError(
                f"Current Strorage: {self.storage}GB, Storage cannot exceed {Tablet.MAX_STORAGE}GB."
            )

        if extra_storage < self.base_storage:
            raise ValueError(
                f"Additinal storage {extra_storage}GB should not be less tha base storage {self.base_storage}GB."
            )

        self._added_storage = extra_storage - self.base_storage

    @model.setter
    def model(self, model_name):
        model_name = model_name.lower().strip()
        if model_name not in Tablet.SUPPORTED_MODELS.keys():
            raise ValueError(f"Model {model_name} is not supported.")
        self._model = model_name

    @storage.setter
    def storage(self, extra_storage):
        self.add_storage(extra_storage)
