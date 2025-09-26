import plotly.graph_objects as go
import numpy as np
from plotly.colors import qualitative

def filter_labels(points, labels, pc1, pc2, min_dist=1.0):
    """Filtra etiquetas para evitar solapamiento excesivo."""
    selected = []
    used_coords = []

    for x, y, label in zip(points[:, pc1], points[:, pc2], labels):
        if all(np.sqrt((x - ux) ** 2 + (y - uy) ** 2) >= min_dist for ux, uy in used_coords):
            selected.append((x, y, label))
            used_coords.append((x, y))

    return selected


import numpy as np
import plotly.graph_objects as go
from plotly.colors import qualitative
import pandas as pd

def scores_plotly(
    data, 
    pca_model, 
    pc1: int, 
    pc2: int, 
    labels: list = None, 
    label_dist: float = 1.0, 
    classes: list = None, 
    cmap: str = 'Viridis',
    original_data: pd.DataFrame = None
):
    """
    2D PCA scores con hover mostrando PC1, PC2, clase, label y valores originales.
    Soporta variables numéricas y categóricas en original_data.
    """
    pc1, pc2 = pc1 - 1, pc2 - 1  # índices base 0
    scores = pca_model.fit_transform(data)
    explained_variance = pca_model.explained_variance_ratio_ * 100

    fig = go.Figure()

    # ==============================
    # Datos para el hover
    # ==============================
    if original_data is not None:
        customdata = original_data.to_numpy()
        feature_names = list(original_data.columns)
        feature_is_numeric = [
            pd.api.types.is_numeric_dtype(original_data[col]) for col in feature_names
        ]
    else:
        customdata = np.array(data)
        feature_names = [f"Var{i+1}" for i in range(data.shape[1])]
        feature_is_numeric = [True] * len(feature_names)  # asumimos numéricos si no hay df

    # -------------------
    # Función para hover
    # -------------------
    def make_hovertemplate(base_template):
        parts = []
        for i, (name, is_num) in enumerate(zip(feature_names, feature_is_numeric)):
            if is_num:
                parts.append(f"{name}: %{{customdata[{i}]:.2f}}")
            else:
                parts.append(f"{name}: %{{customdata[{i}]}}")
        variables_template = "<br>".join(parts)
        return base_template + "<br>" + variables_template + "<extra></extra>"

    # -------------------
    # Puntos coloreados
    # -------------------
    if classes is not None:
        classes = np.array(classes)
        if classes.dtype.kind in {"U", "S", "O"} or len(np.unique(classes)) < 10:
            unique_classes = np.unique(classes)
            colors = qualitative.Plotly
            for i, cls in enumerate(unique_classes):
                mask = classes == cls
                hover_labels = [labels[j] if labels is not None else '' for j, m in enumerate(mask) if m]
                fig.add_trace(go.Scatter(
                    x=scores[mask, pc1],
                    y=scores[mask, pc2],
                    mode="markers",
                    marker=dict(size=8, color=colors[i % len(colors)],
                                line=dict(width=0.5, color="black")),
                    name=str(cls),
                    text=hover_labels,
                    customdata=customdata[mask],
                    hovertemplate=make_hovertemplate(
                        "%{text}<br>"
                        f"class: {cls}<br>"
                        f"PC{pc1+1}: %{{x:.3f}}<br>"
                        f"PC{pc2+1}: %{{y:.3f}}"
                    )
                ))
        else:
            hover_labels = labels if labels is not None else ['']*len(scores)
            fig.add_trace(go.Scatter(
                x=scores[:, pc1],
                y=scores[:, pc2],
                mode="markers",
                marker=dict(size=8, color=classes, colorscale=cmap, showscale=True,
                            line=dict(width=0.5, color="black")),
                name="",
                text=hover_labels,
                customdata=customdata,
                hovertemplate=make_hovertemplate(
                    f"PC{pc1+1}: %{{x:.3f}}<br>"
                    f"PC{pc2+1}: %{{y:.3f}}<br>"
                    "Clase: %{marker.color}<br>"
                    "Label: %{text}"
                )
            ))
    else:
        hover_labels = labels if labels is not None else ['']*len(scores)
        fig.add_trace(go.Scatter(
            x=scores[:, pc1],
            y=scores[:, pc2],
            mode="markers",
            marker=dict(size=8, color="blue", opacity=0.8,
                        line=dict(width=0.5, color="black")),
            name="",
            text=hover_labels,
            customdata=customdata,
            hovertemplate=make_hovertemplate(
                "PC{}: %{x:.3f}<br>PC{}: %{y:.3f}<br>Label: %{text}".format(pc1+1, pc2+1)
            )
        ))

    # Ejes en cero
    fig.add_shape(type="line",
                  x0=min(scores[:, pc1]), x1=max(scores[:, pc1]),
                  y0=0, y1=0,
                  line=dict(color="black", dash="dash"))
    fig.add_shape(type="line",
                  x0=0, x1=0,
                  y0=min(scores[:, pc2]), y1=max(scores[:, pc2]),
                  line=dict(color="black", dash="dash"))

    # Layout
    fig.update_layout(
        title="2D Scores",
        xaxis=dict(
            title=f'PC{pc1+1} ({explained_variance[pc1]:.2f}%)',
            zeroline=False
        ),
        yaxis=dict(
            title=f'PC{pc2+1} ({explained_variance[pc2]:.2f}%)',
            zeroline=False
        ),
        template="plotly_white",
        width=900,
        height=700
    )

    return fig



import plotly.graph_objects as go
import numpy as np
from plotly.colors import qualitative

def loadings_plotly(pca_model, pc1: int, pc2: int, labels: list = None, 
                    label_dist: float = 0.01, classes: list = None, cmap: str = 'Viridis'):
    """
    2D PCA loadings con hover personalizado mostrando PC1, PC2, clase y label.
    """
    pc1, pc2 = pc1 - 1, pc2 - 1  # indices base 0
    loadings = pca_model.components_
    explained_variance = pca_model.explained_variance_ratio_ * 100

    fig = go.Figure()

    # Filtrar etiquetas si se proporcionan
    filtered_labels = None
    if labels is not None:
        filtered = filter_labels(loadings, labels, pc1, pc2, min_dist=label_dist)
        if filtered:
            xs, ys, filtered_labels = zip(*filtered)
        else:
            xs, ys, filtered_labels = [], [], []

    # -------------------
    # Puntos coloreados
    # -------------------
    if classes is not None:
        classes = np.array(classes)
        if classes.dtype.kind in {"U", "S", "O"} or len(np.unique(classes)) < 10:
            unique_classes = np.unique(classes)
            colors = qualitative.Plotly
            for i, cls in enumerate(unique_classes):
                mask = classes == cls
                hover_labels = [labels[j] if labels is not None else '' for j, m in enumerate(mask) if m]
                fig.add_trace(go.Scatter(
                    x=loadings[pc1][mask],
                    y=loadings[pc2][mask],
                    mode="markers",
                    marker=dict(size=8, color=colors[i % len(colors)],
                                line=dict(width=0.5, color="black")),
                    name="",
                    text=hover_labels,
                    hovertemplate = (
                        "%{text}<br>"
                        f"class: {cls}<br>"
                        f"PC{pc1+1}: %{{x:.3f}}<br>"
                        f"PC{pc2+1}: %{{y:.3f}}"
                    )
                ))
        else:
            hover_labels = labels if labels is not None else ['']*loadings.shape[1]
            fig.add_trace(go.Scatter(
                x=loadings[pc1],
                y=loadings[pc2],
                mode="markers",
                marker=dict(size=8, color=classes, colorscale=cmap, showscale=True,
                            line=dict(width=0.5, color="black")),
                name="",
                text=hover_labels,
                hovertemplate=(
                    "%{text}"
                    "class: %{marker.color}<br>"
                    f"PC{pc1+1}: %{{x:.3f}}<br>"
                    f"PC{pc2+1}: %{{y:.3f}}<br>"
                )
            ))
    else:
        hover_labels = labels if labels is not None else ['']*loadings.shape[1]
        fig.add_trace(go.Scatter(
            x=loadings[pc1],
            y=loadings[pc2],
            mode="markers",
            marker=dict(size=8, color="blue", opacity=0.8,
                        line=dict(width=0.5, color="black")),
            name="",
            text=hover_labels,
            hovertemplate=(
                "%{text}<br>"
                f"PC{pc1+1}: %{{x:.3f}}<br>"
                f"PC{pc2+1}: %{{y:.3f}}"
            )
        ))

    # Ejes en cero
    fig.add_shape(type="line",
                  x0=min(loadings[pc1]), x1=max(loadings[pc1]),
                  y0=0, y1=0,
                  line=dict(color="black", dash="dash"))
    fig.add_shape(type="line",
                  x0=0, x1=0,
                  y0=min(loadings[pc2]), y1=max(loadings[pc2]),
                  line=dict(color="black", dash="dash"))

    # Layout
    fig.update_layout(
        title="2D Loadings",
        xaxis=dict(
            title=f'PC{pc1+1} ({explained_variance[pc1]:.2f}%)',
            zeroline=False
        ),
        yaxis=dict(
            title=f'PC{pc2+1} ({explained_variance[pc2]:.2f}%)',
            zeroline=False
        ),
        template="plotly_white",
        width=800,
        height=600
    )

    return fig
