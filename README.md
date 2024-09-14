# Arbitrage Betting Model

## Project Overview

This repository contains a model for detecting **arbitrage betting opportunities** in tennis matches by comparing odds from multiple bookmakers. By leveraging differences in odds for the same events across different betting platforms, this script identifies "sure bets" — situations where it's possible to guarantee a profit, regardless of the outcome of the match. This is a practical implementation of an arbitrage strategy, applied in real-time using data from major betting sites.

## Arbitrage Betting Explanation

Arbitrage betting involves placing bets on all possible outcomes of a sporting event using odds from different bookmakers. By selecting the right combination of bets, a profit can be guaranteed, no matter which outcome occurs.

In a tennis match, there are two possible outcomes: either Player 1 or Player 2 wins. An arbitrage opportunity exists if the sum of the inverses of the odds for each player is less than 1:

$$ \frac{1}{\text{odds for Player 1}} + \frac{1}{\text{odds for Player 2}} < 1 $$

When this condition is met, we can distribute bets in such a way that the total payout will always be greater than the total stake, regardless of the result.



## Optimal Bet Allocation

The goal is to distribute the total stake in such a way that the payout remains the same no matter which outcome wins. The formula for the optimal bet allocation is based on the odds for both outcomes:

1. Let’s assume you want to bet a total of **S** (e.g., 1€) on Outcome 1 with odds \(O1\), and Outcome 2 has odds \(O2\).

2. The bet allocation for Outcome 2 is:
   $$ S_{\text{Outcome 2}} = S \times \frac{O1}{O2} $$

4. The guaranteed payout will be the same for both outcomes:
   $$ \text{Payout} = S_{\text{Outcome 1}} \times O1 = S_{\text{Outcome 2}} \times O2 $$

5. The profit is calculated as:
   $$ \text{Profit} = \text{Payout} - \left(S_{\text{Outcome 1}} + S_{\text{Outcome 2}}\right) $$

## Future Enhancements

This project can be expanded in the following ways:

1.  **Include More Websites**: Adding odds from more bookmakers would increase the chances of finding arbitrage opportunities and provide a more comprehensive model.
    
2.  **Expand to Other Sports**: Although the current model focuses on tennis, the script can be adapted to handle sports with more than two possible outcomes (e.g., football, where a match can end in a win, draw, or loss). The equation would be expanded to:
    
    $$ \frac{1}{\text{odds for Outcome 1}} + \frac{1}{\text{odds for Outcome 2}} + \frac{1}{\text{odds for Outcome 3}} < 1 $$

3.  **Automate Bet Placement**: Integrate APIs from bookmakers to automatically place bets when arbitrage opportunities are detected. This may be complex since the HTML structure of betting websites frequently changes, but automating this process would bring the project closer to a fully operational arbitrage system.

## Example Output

```plaintext
Match: Federer vs Nadal
Odds from Betfair: 2.10 (Federer) and from Bwin: 2.15 (Nadal)
Place 1€ bet on Federer (Betfair) and 0.98€ on Nadal (Bwin)
Guaranteed payout: 2.10€
Guaranteed profit: 0.12€
