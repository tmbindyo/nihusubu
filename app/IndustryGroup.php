<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class IndustryGroup extends Model
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
    public function sector()
    {
        return $this->belongsTo('App\Sector');
    }

    // Children
    public function industries()
    {
        return $this->hasMany('App\Industry');
    }
}
