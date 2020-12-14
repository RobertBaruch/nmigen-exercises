# Challenge #1: The "hardest Sudoku puzzle in the world"

[Sudoku](https://en.wikipedia.org/wiki/Sudoku) is a puzzle, typically on a 9x9 grid made up of nine 3x3 subgrids, where every row and column must contain every number between 1 and 9, exactly once, and every 3x3 subgrid also contains every number exactly once. Some squares in the puzzle are already filled out, which act as constraints. The rest are blank, and need to be filled in through logical reasoning. The solution is unique.

Write a module and use formal verification to solve the ["hardest Sudoku puzzle in the world"](https://gizmodo.com/can-you-solve-the-10-hardest-logic-puzzles-ever-created-1064112665).

<style>
table { border-collapse: collapse; font-family: Calibri, sans-serif; }
colgroup, tbody { border: solid medium; }
td { border: solid thin; height: 1.4em; width: 1.4em; text-align: center; padding: 0; }
</style>
<table>
  <caption>The hardest Sudoku puzzle in the world</caption>
  <colgroup border="solid medium"><col><col><col>
  <colgroup border="solid medium"><col><col><col>
  <colgroup border="solid medium"><col><col><col>
  <tbody>
   <tr> <td>8 <td>  <td>  <td>  <td>  <td>  <td>  <td>  <td>
   <tr> <td>  <td>  <td>3 <td>6 <td>  <td>  <td>  <td>  <td>
   <tr> <td>  <td>7 <td>  <td>  <td>9 <td>  <td>2 <td>  <td>
  <tbody>
   <tr> <td>  <td>5 <td>  <td>  <td>  <td>7 <td>  <td>  <td>
   <tr> <td>  <td>  <td>  <td>  <td>4 <td>5 <td>7 <td>  <td>
   <tr> <td>  <td>  <td>  <td>1 <td>  <td>  <td>  <td>3 <td>
  <tbody>
   <tr> <td>  <td>  <td>1 <td>  <td>  <td>  <td>  <td>6 <td>8
   <tr> <td>  <td>  <td>8 <td>5 <td>  <td>  <td>  <td>1 <td>
   <tr> <td>  <td>9 <td>  <td>  <td>  <td>  <td>4 <td>  <td>
</table>
