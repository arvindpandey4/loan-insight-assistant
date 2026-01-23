export const queryLoanInsights = async (question) => {
  console.log("Sending to backend:", question);
  
  await new Promise((resolve) => setTimeout(resolve, 1500));

  return {
    similar_cases_found: 11,
    common_risk_factors: [
      "Credit score below internal threshold",
      "High EMI to income ratio",
    ],
    historical_trend: "72% of similar cases were rejected",
    explanation:
      "Applicants with similar income and credit profiles were commonly rejected due to elevated repayment risk observed in historical data.",
    confidence: 0.79,
  };
};