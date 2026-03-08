#!/usr/bin/env python3
"""Apply the study-owned `iaddq` patches to restored official HCL templates."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_exact_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise ValueError(f"patch anchor not found:\n{old}")
    return text.replace(old, new, 1)


def patch_seq(path: Path) -> None:
    text = path.read_text()
    replacements = [
        (
            "bool instr_valid = icode in \n"
            "\t{ INOP, IHALT, IRRMOVQ, IIRMOVQ, IRMMOVQ, IMRMOVQ,\n"
            "\t       IOPQ, IJXX, ICALL, IRET, IPUSHQ, IPOPQ };",
            "bool instr_valid = icode in \n"
            "\t{ INOP, IHALT, IRRMOVQ, IIRMOVQ, IRMMOVQ, IMRMOVQ,\n"
            "\t       IOPQ, IJXX, ICALL, IRET, IPUSHQ, IPOPQ, IIADDQ };",
        ),
        (
            "bool need_regids =\n"
            "\ticode in { IRRMOVQ, IOPQ, IPUSHQ, IPOPQ, \n"
            "\t\t     IIRMOVQ, IRMMOVQ, IMRMOVQ };",
            "bool need_regids =\n"
            "\ticode in { IRRMOVQ, IOPQ, IPUSHQ, IPOPQ, \n"
            "\t\t     IIRMOVQ, IRMMOVQ, IMRMOVQ, IIADDQ };",
        ),
        (
            "bool need_valC =\n"
            "\ticode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IJXX, ICALL };",
            "bool need_valC =\n"
            "\ticode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IJXX, ICALL, IIADDQ };",
        ),
        (
            "word srcB = [\n"
            "\ticode in { IOPQ, IRMMOVQ, IMRMOVQ  } : rB;",
            "word srcB = [\n"
            "\ticode in { IOPQ, IRMMOVQ, IMRMOVQ, IIADDQ } : rB;",
        ),
        (
            "word dstE = [\n"
            "\ticode in { IRRMOVQ } && Cnd : rB;\n"
            "\ticode in { IIRMOVQ, IOPQ} : rB;",
            "word dstE = [\n"
            "\ticode in { IRRMOVQ } && Cnd : rB;\n"
            "\ticode in { IIRMOVQ, IOPQ, IIADDQ } : rB;",
        ),
        (
            "word aluA = [\n"
            "\ticode in { IRRMOVQ, IOPQ } : valA;\n"
            "\ticode in { IIRMOVQ, IRMMOVQ, IMRMOVQ } : valC;",
            "word aluA = [\n"
            "\ticode in { IRRMOVQ, IOPQ } : valA;\n"
            "\ticode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IIADDQ } : valC;",
        ),
        (
            "word aluB = [\n"
            "\ticode in { IRMMOVQ, IMRMOVQ, IOPQ, ICALL, \n"
            "\t\t      IPUSHQ, IRET, IPOPQ } : valB;",
            "word aluB = [\n"
            "\ticode in { IRMMOVQ, IMRMOVQ, IOPQ, ICALL, \n"
            "\t\t      IPUSHQ, IRET, IPOPQ, IIADDQ } : valB;",
        ),
        (
            "bool set_cc = icode in { IOPQ };",
            "bool set_cc = icode in { IOPQ, IIADDQ };",
        ),
    ]
    for old, new in replacements:
        text = replace_exact_once(text, old, new)
    path.write_text(text)


def patch_pipe(path: Path) -> None:
    text = path.read_text()
    replacements = [
        (
            "bool instr_valid = f_icode in \n"
            "\t{ INOP, IHALT, IRRMOVQ, IIRMOVQ, IRMMOVQ, IMRMOVQ,\n"
            "\t  IOPQ, IJXX, ICALL, IRET, IPUSHQ, IPOPQ };",
            "bool instr_valid = f_icode in \n"
            "\t{ INOP, IHALT, IRRMOVQ, IIRMOVQ, IRMMOVQ, IMRMOVQ,\n"
            "\t  IOPQ, IJXX, ICALL, IRET, IPUSHQ, IPOPQ, IIADDQ };",
        ),
        (
            "bool need_regids =\n"
            "\tf_icode in { IRRMOVQ, IOPQ, IPUSHQ, IPOPQ, \n"
            "\t\t     IIRMOVQ, IRMMOVQ, IMRMOVQ };",
            "bool need_regids =\n"
            "\tf_icode in { IRRMOVQ, IOPQ, IPUSHQ, IPOPQ, \n"
            "\t\t     IIRMOVQ, IRMMOVQ, IMRMOVQ, IIADDQ };",
        ),
        (
            "bool need_valC =\n"
            "\tf_icode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IJXX, ICALL };",
            "bool need_valC =\n"
            "\tf_icode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IJXX, ICALL, IIADDQ };",
        ),
        (
            "word d_srcB = [\n"
            "\tD_icode in { IOPQ, IRMMOVQ, IMRMOVQ  } : D_rB;",
            "word d_srcB = [\n"
            "\tD_icode in { IOPQ, IRMMOVQ, IMRMOVQ, IIADDQ } : D_rB;",
        ),
        (
            "word d_dstE = [\n"
            "\tD_icode in { IRRMOVQ, IIRMOVQ, IOPQ} : D_rB;",
            "word d_dstE = [\n"
            "\tD_icode in { IRRMOVQ, IIRMOVQ, IOPQ, IIADDQ } : D_rB;",
        ),
        (
            "word aluA = [\n"
            "\tE_icode in { IRRMOVQ, IOPQ } : E_valA;\n"
            "\tE_icode in { IIRMOVQ, IRMMOVQ, IMRMOVQ } : E_valC;",
            "word aluA = [\n"
            "\tE_icode in { IRRMOVQ, IOPQ } : E_valA;\n"
            "\tE_icode in { IIRMOVQ, IRMMOVQ, IMRMOVQ, IIADDQ } : E_valC;",
        ),
        (
            "word aluB = [\n"
            "\tE_icode in { IRMMOVQ, IMRMOVQ, IOPQ, ICALL, \n"
            "\t\t     IPUSHQ, IRET, IPOPQ } : E_valB;",
            "word aluB = [\n"
            "\tE_icode in { IRMMOVQ, IMRMOVQ, IOPQ, ICALL, \n"
            "\t\t     IPUSHQ, IRET, IPOPQ, IIADDQ } : E_valB;",
        ),
        (
            "bool set_cc = E_icode == IOPQ &&",
            "bool set_cc = E_icode in { IOPQ, IIADDQ } &&",
        ),
    ]
    for old, new in replacements:
        text = replace_exact_once(text, old, new)
    path.write_text(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("seq_hcl", type=Path)
    parser.add_argument("pipe_hcl", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    patch_seq(args.seq_hcl)
    patch_pipe(args.pipe_hcl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
