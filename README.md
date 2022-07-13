# Ttm api documentation

Let's go

```python
    # du python ici pour le back
    print('Bonjour ttm')
```

```typescript
    // typescript pour le front
    const e = (e : string)=>{
        console.log(` bonjour ttm ${b}`)
    }
```

# Routing new concept

S est la ville de depart,
A,B, sont les arrets (escales )
F ville d'arriver

```mermaid
flowchart LR
    S -->A;
    A-->S;
    B -->A;
    A-->B;
    F -->B;
    B-->F;
```

```mermaid
flowchart LR
    S -->A;
    A-->S;
```

# Diangramme Design last update

la comision est valable si une entreprise vent pour un autre entreprise (en %)
### NB (en %)
frais des services
taxe
comissions


```mermaid
classDiagram
    class JourneyClass{
        code : String
        name : String

    }

    class Tarif{
        journey_class : JourneyClass
        route : Routing
        devise : CDF|USD
        frai_service : Float
        comission: Float
        adult: Float
        child : Float
        baby : Float
        taxe : Float
        actif : Boolean
        Ptc : = base +taxe+ frai_service - comission
    }

    class Routing{
        company: ID
        node: CoverCity
        whereFrom: Routing
        whereTo: Routing
        distance: Float
    }

    class Journey{

    }
```
