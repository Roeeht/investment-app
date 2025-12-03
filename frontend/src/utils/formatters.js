// Utility functions for formatting data

export const formatCurrency = (amount) => {
  if (amount == null || isNaN(amount)) return "$0.00";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
};

export const formatPercentage = (value) => {
  if (value == null || isNaN(value)) return "0%";
  return `${(value * 100).toFixed(2)}%`;
};

export const formatDate = (date) => {
  if (!date) return "";
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export const calculateChange = (current, previous) => {
  if (!current || !previous) return 0;
  return ((current - previous) / previous) * 100;
};
