<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Issue extends Model
{
    use SoftDeletes, UuidTrait;
    public $incrementing = false;

    // Parents
    public function status()
    {
        return $this->belongsTo('App\Status');
    }
    public function user()
    {
        return $this->belongsTo('App\User');
    }
    public function project()
    {
        return $this->belongsTo('App\Project');
    }
    public function milestone()
    {
        return $this->belongsTo('App\Milestone');
    }
    public function task()
    {
        return $this->belongsTo('App\Task');
    }
    public function reporter()
    {
        return $this->belongsTo('App\User','reporter_id','id');
    }
    public function assignee()
    {
        return $this->belongsTo('App\User','assignee_id','id');
    }
    public function assigned_issue()
    {
        return $this->belongsTo('App\User','assignee_id','id');
    }
    public function reported_issue()
    {
        return $this->belongsTo('App\User','assignee_id','id');
    }

    // Children
    public function timesheets()
    {
        return $this->hasMany('App\Timesheet');
    }
    public function issue_uploads()
    {
        return $this->hasMany('App\IssueUpload');
    }
}
