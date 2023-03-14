
from language_model.named_transformers_model import NamedModel


def test_gpt2_instruct_model():
    model_name = "SummerSigh/GPT2-Instruct-SFT"
    model = NamedModel(model_name)
    actual = model.complete("What search term would I use if I wanted to find the akka library for scala")
    assert actual == "akka"