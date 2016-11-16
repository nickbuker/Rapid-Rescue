# Experements with Poisson regression.
library(ggplot2)

N <- 100000

df <- data.frame(
  x_1 = runif(N, -1, 1), x_2 = runif(N, -1, 1),
  expos = runif(N)
)

df$lp <- 1 + 0.5*df$x_1 - df$x_2
df$mu <- exp(df$lp)
df$mu_expos = df$mu * df$expos
df$y <- unlist(
  lapply(df$mu_expos, function(x) rpois(1, lambda=x)))

ggplot() + geom_density(aes(x=df$y))

M <- glm(y ~ x_1 + x_2 + offset(log(expos)),
         data=df, family=poisson(link='log'))

summary(M, dispersion=1)
