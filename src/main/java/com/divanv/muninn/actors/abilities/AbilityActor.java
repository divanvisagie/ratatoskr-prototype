package com.divanv.muninn.actors.abilities;

import com.divanv.muninn.actors.core.ChildAwareActor;

public abstract class AbilityActor extends ChildAwareActor {

    protected String description = "This ability is currently disabled or ignored on purpose";

    public String getDescription() {
        return description;
    }
}
