        # Problem: Meldable Heap Bridge (0x13)

        ## Problem Statement

        Manage multiple named heaps with MAKE/PUSH/MELD/POP commands. After MELD A B, heap B becomes empty.

        ## Input

        - Line 1: command count q
- Next q lines: commands MAKE name, PUSH name x, MELD dst src, POP name

        ## Output

        For each POP command, print the minimum key or EMPTY.

        ## Fixtures

        - `input1.txt`
- `input2.txt`

        ## Source

        Repo-authored study problem derived from CLRS Ch 19.
