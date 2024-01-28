import src.domain.short_code_generator as generator


def test_generator_by_default_return_code_with_len_8():
    assert len(generator.generate()) == 8


def test_generator_with_param_7_generate_code_with_len_7():
    assert len(generator.generate(length=7)) == 7


def test_generator_return_different_codes():
    codes = [generator.generate() for _ in range(10)]
    assert len(codes) == len(set(codes))
