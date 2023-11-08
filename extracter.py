import re
from typing import Union


def extract_finance(args, text):
    pattern = '-?\d+\.?\d*%?'
    if pred := re.findall(pattern, text):
        return eval(f'{pred[-1][:-1]}/100') if pred[-1][-1] == '%' else float(pred[-1])
    pattern = 'yes|no'
    return pred[-1] if (pred := re.findall(pattern, text)) else None


def extract_answer(args, text):
    dataset = args.dataset.lower()
    if dataset in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
        pred_answer = extract_number(args, text)
    elif dataset == "commonsenseqa":
        pred = text.strip()
        pred = re.sub("\(|\)|\:|\.|\,", "", pred)
        pred = pred.split()
        return [i for i in pred if i in ('A|B|C|D|E')][-1]
    elif dataset == "aqua":
        pred = text.strip()
        return re.findall(r'A|B|C|D|E', pred)[0]
    elif dataset in ["strategyqa", 'coin_flip']:
        pred = text.lower()
        pred = re.sub("\"|\'|\n|\.|\s|\:|\,", " ", pred)
        pred = pred.split()
        return [i for i in pred if i in ("yes", "no")][-1]
    elif dataset == "last_letters":
        return re.sub("\"|\'|\n|\.|\s", "", text)
    else:
        raise NotImplementedError(f' not support dataset: {dataset}')
    if isinstance(pred_answer, str):
        try:
            pred_answer = float(pred_answer)
        except ValueError as e:
            pred_answer = float('inf')
    return pred_answer


def get_precision(gt_ans: float) -> int:
    return len(str(gt_ans).split('.')[-1]) if '.' in str(gt_ans) else 5


def extract_bool(args, text: str) -> str:
    pass


def extract_number(args, text: str) -> Union[float, None]:
    text = text.replace(',', '')
    return (
        float(pred[-1])
        if (pred := list(re.findall(r'-?\d+\.?\d*', text)))
        else None
    )


def extract_choice(args, text: str) -> str:
    pass
