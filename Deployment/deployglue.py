#!/usr/bin/env python3
from aws_cdk import core

from Stacks.glue_project_stack import ScheduledGlueJob #GlueProjectStack


app = core.App()
#GlueProjectStack(app, "GlueProject")
ScheduledGlueJob(app, "GlueProject");
app.synth()
