import pytest

from config import StageConfig, StageSchema




def test_create_stage_config():
  
    result = StageSchema().load({
        "pipelines": ["Platform.test", "Platform.test2"],
        "dependsOn": "basic_infra"
       
    })

    assert result == StageConfig(["Platform.test", "Platform.test2"],"basic_infra")
