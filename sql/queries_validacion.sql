
-- 1. Validación básica: Contar total de filas
SELECT 
    COUNT(*) as total_filas
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`;


-- 2. Ver primeros 10 registros
SELECT *
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
ORDER BY wrapped_2025_rank
LIMIT 10;


-- 3. Top 5 artistas por número de oyentes
SELECT 
    wrapped_2025_rank,
    artist_name,
    monthly_listeners_millions_mar2026,
    primary_genre,
    country
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
ORDER BY monthly_listeners_millions_mar2026 DESC
LIMIT 5;


-- 4. Promedio de oyentes por género musical
SELECT 
    primary_genre,
    COUNT(*) as total_artistas,
    ROUND(AVG(monthly_listeners_millions_mar2026), 2) as promedio_oyentes_millones,
    ROUND(MIN(monthly_listeners_millions_mar2026), 2) as min_oyentes,
    ROUND(MAX(monthly_listeners_millions_mar2026), 2) as max_oyentes
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
GROUP BY primary_genre
ORDER BY promedio_oyentes_millones DESC;


-- 5. Artistas con Grammy vs sin Grammy
SELECT 
    CASE 
        WHEN grammy_wins > 0 THEN 'Con Grammy' 
        ELSE 'Sin Grammy' 
    END as categoria_grammy,
    COUNT(*) as total_artistas,
    ROUND(AVG(monthly_listeners_millions_mar2026), 2) as promedio_oyentes_millones,
    ROUND(AVG(followers_millions), 2) as promedio_seguidores_millones
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
GROUP BY categoria_grammy
ORDER BY promedio_oyentes_millones DESC;


-- 6. Distribución de artistas por país
SELECT 
    country,
    COUNT(*) as total_artistas,
    ROUND(AVG(monthly_listeners_millions_mar2026), 2) as promedio_oyentes
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
GROUP BY country
ORDER BY total_artistas DESC;



-- 7. Artistas por década de debut
SELECT 
    FLOOR(debut_year / 10) * 10 as decada_debut,
    COUNT(*) as total_artistas,
    ROUND(AVG(monthly_listeners_millions_mar2026), 2) as promedio_oyentes
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
GROUP BY decada_debut
ORDER BY decada_debut DESC;


-- 8. Artistas con más seguidores vs más oyentes
SELECT 
    artist_name,
    monthly_listeners_millions_mar2026,
    followers_millions,
    ROUND(monthly_listeners_millions_mar2026 / followers_millions, 2) as ratio_oyentes_seguidores
FROM `proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists`
ORDER BY ratio_oyentes_seguidores DESC
LIMIT 10;

